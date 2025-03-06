import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, ContextTypes, Application

from Database.database import Wallet

from Database import db, Settings, User
from Config import Configs

class SetWallet(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        
        self.agree_step = int(f"{self.step_conversation}1")
    
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
        
    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
        
        steps[self.agree_step] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_agree),
            ]
        return steps
        
    async def on_query_receive(self,update: Update, context: CallbackContext):
        await update.message.chat.send_message("Enter your wallet Address:")
        
        return self.agree_step

    async def on_receive_agree(self,update: Update, context: CallbackContext):
        new_wallet_address = update.message.text
        
        context.user_data["wallet"] = new_wallet_address
        
        await update.message.reply_text(f"Type OK to Update Wallet Address: {new_wallet_address}")
        
        return self.step_conversation
        
    async def on_receive_input(self,update: Update, context: CallbackContext):       
        user_data = context.user_data
        user_id = update.effective_user.id

        new_wallet_address = user_data["wallet"]
        
        if update.message.text == "OK":
            
            with db.session_scope() as session:

                if not Configs.is_admin(update.message.from_user.id):
                    user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
                    wallet = session.query(Wallet).filter_by(current_walletaddress=f"{new_wallet_address}").first()

                    if wallet !=None:
                        message = self.get_text(context, "exist_wallet")
                        await update.message.reply_text(message)
                        return

                    if user != None:
                        wallet = session.query(Wallet).filter_by(userId=user.id).one_or_none()
                        wallet.current_walletaddress = new_wallet_address
                else:
                    settings = session.query(Settings).one()
                    settings.walletAddress = new_wallet_address
            
            await update.message.reply_text(f"Wallet address updated to {new_wallet_address}")

        if self.cancel is not None:
            return await self.cancel(update, context)
        
        return ConversationHandler.END