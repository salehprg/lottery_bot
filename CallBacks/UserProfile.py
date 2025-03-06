import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, Application, ConversationHandler, CallbackQueryHandler
from Database import db, User,Wallet

class UserProfile(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
    

    async def on_query_receive(self, update: Update, context: CallbackContext):
        
        user_id = update.effective_user.id
        
        user = None
        wallet = None
        profileinfo = ""
        
        with db.session_scope() as session:
            user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
            if user != None:
                session.refresh(user)
                wallet = user.wallet[0]

            wallet_address = "N/A"
            if wallet.current_walletaddress != None:
                wallet_address = wallet.current_walletaddress

            profileinfo = self.get_text(context, "profile").format(user_id= user.telegramId, balance=wallet.balance, wallet_address= wallet_address)

        await update.message.chat.send_message(profileinfo)
        
        return ConversationHandler.END
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass