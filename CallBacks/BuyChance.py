from datetime import datetime
import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from telegram.constants import ParseMode
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters,Application,CallbackQueryHandler,ConversationHandler
from Database import db, Settings
from Database.database import Lottery, LotteryUser, User
from sqlalchemy import func

class BuyChance(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        
    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
        
        return steps

    def create_handlers(self, application : Application, cancel):
        self.cancel = cancel
        
        regex_pattern = self.get_regex_pattern()
        entry_handler = MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(regex_pattern), self.on_query_receive)

        states = {}
        states = self.on_conv_step(states)

        application.add_handler(ConversationHandler(
            entry_points=[entry_handler],  # The conversation is triggered by the inline button, not a direct command
            states=states,
            fallbacks=[CallbackQueryHandler(self.cancel)],
            per_message=False
        ))

    async def on_query_receive(self, update: Update, context: CallbackContext):
        
        user_id = update.effective_user.id
        
        mainwalletAddress = None
        current_chance = 0
        wallet_balance = 0
        user_wallet_address = None

        with db.session_scope() as session:
            settings = session.query(Settings).one()
            exist_user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
            lottery = session.query(Lottery).filter(Lottery.startDate > datetime.now()).order_by(Lottery.startDate).one_or_none()

            if lottery is None:
                await update.message.chat.send_message(f"Currently there isnt any Lottery!")
                return ConversationHandler.END
            
            lottery_user = session.query(LotteryUser).filter_by(userId=f"{exist_user.id}", lotteryId=f"{lottery.id}").first()
            if lottery_user is not None:
                current_chance = session.query(func.sum(LotteryUser.ticketAmount)).filter_by(
                                userId=f"{exist_user.id}",
                                lotteryId=f"{lottery.id}"
                            ).scalar()
                            
            mainwalletAddress = settings.walletAddress

            session.refresh(exist_user)
            wallet_balance = exist_user.wallet[0].balance

            if exist_user.wallet[0].current_walletaddress == None:
                message_empty = self.get_text(context, "empty_wallet")
                await update.message.chat.send_message(message_empty, parse_mode=ParseMode.HTML)
                return ConversationHandler.END

        message = self.get_text(context, "buy_chance").format(current_chance=current_chance, wallet_balance=wallet_balance)

        await update.message.chat.send_message(message, parse_mode=ParseMode.HTML)
        
        return self.step_conversation
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        user_id = update.effective_user.id

        try:
            chance_float = float(update.message.text)
        except (ValueError, TypeError):
            await update.message.chat.send_message(f"Please enter valid amount")
            return ConversationHandler.END

        if chance_float <= 0:
            await update.message.chat.send_message(f"Please enter amount greater than 0")
            return self.step_conversation
        
        total_amount = 0
        lottery_date = None

        with db.session_scope() as session:
            exist_user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
            lottery = session.query(Lottery).filter(Lottery.startDate > datetime.now()).order_by(Lottery.startDate).one_or_none()
            
            if lottery is None:
                await update.message.chat.send_message(f"Currently there isnt any Lottery!")
                return ConversationHandler.END
            
            session.refresh(exist_user)
            wallet_balance = exist_user.wallet[0].balance
            if wallet_balance < chance_float:
                await update.message.chat.send_message(f"Insufficient amount")
                return self.step_conversation

            lottery_user = LotteryUser()
            lottery_user.lotteryId = lottery.id
            lottery_user.ticketAmount = chance_float
            lottery_user.userId = exist_user.id
            lottery_user.buyDate = datetime.now()
            # lottery.userCount += 1

            session.add(lottery_user)
            session.flush()
            
            total_amount = session.query(func.sum(LotteryUser.ticketAmount)).filter_by(
                                userId=f"{exist_user.id}",
                                lotteryId=f"{lottery.id}"
                            ).scalar()
            
            lottery.poolSize += chance_float

            exist_user.wallet[0].balance -= chance_float

            lottery_date = lottery.startDate
            total_chance = total_amount

        message = self.get_text(context, "succed_buy").format(chance_float=chance_float, total_chance=total_chance)

        await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
        return ConversationHandler.END