from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, Application, ConversationHandler, CallbackQueryHandler
from Database import db, User,Wallet

class UserProfile(BaseClassAction):
    def __init__(self, step_conversation, callback_data):
        super().__init__(step_conversation=step_conversation,
                         callback_data=callback_data)
        
    def on_conv_step(self, steps : dict):
        pass
    
    def create_handlers(self, application : Application, cancel):
        self.cancel = cancel
        application.add_handler(CallbackQueryHandler(self.on_query_receive, pattern=self.callback_pattern))

    def on_menu_generate(self, keys : list):
        keyboard = [InlineKeyboardButton("My Profile", callback_data=self.callback_data)]
        
        keys.append(keyboard)
        return keys

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

            profileinfo = f"""شماره کاربر: {user.telegramId}\nموجودی: {wallet.balance}"""

        await update.callback_query.edit_message_text(profileinfo)
        
        return ConversationHandler.END
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass