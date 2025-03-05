import re
from sqlalchemy import func
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, Application, ConversationHandler, CallbackQueryHandler
from Database import db, User,Wallet
from Database.database import Lottery, LotteryUser
from telegram.constants import ParseMode

class ViewLotteryResult(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
    

    def get_user_lottery_history(self, user_id):
        with db.session_scope() as session:
            
            results = session.query(
                Lottery.startDate,
                Lottery.winnerId,
                func.sum(LotteryUser.ticketAmount).label('purchasedAmount')
            ).join(Lottery, Lottery.id == LotteryUser.lotteryId)\
            .filter(LotteryUser.userId == user_id)\
            .group_by(Lottery.startDate, Lottery.winnerId)\
            .all()
            
            # Build a dictionary mapping lottery_date -> {"purchasedAmount": ..., "winnerId": ...}
            history = {
                str(start_date): {
                    "purchasedAmount": purchasedAmount,
                    "winnerId": winnerId
                }
                for start_date, winnerId, purchasedAmount in results
            }
            
            return history

    async def on_query_receive(self, update: Update, context: CallbackContext):
        
        user_id = update.effective_user.id
        
        user = None
        message = ""
        
        with db.session_scope() as session:
            user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
            history_map = self.get_user_lottery_history(user.id)

            for history in history_map:
                amount = history_map[history]['purchasedAmount']
                winnerId = history_map[history]['winnerId']

                win_text = ""
                if winnerId == user.id:
                    win_text = "<i>You are winner !</i>"
                else:
                    win_text = "You have not won"

                message += f"Lottery date <strong>{history}</strong>  Amount: <strong>{amount}</strong> {win_text}\n"

        await update.message.chat.send_message(message, parse_mode=ParseMode.HTML)
        
        return ConversationHandler.END
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass