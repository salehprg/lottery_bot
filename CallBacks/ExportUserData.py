from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters,Application,CallbackQueryHandler
from Database.database import db,User
from utils import export_to_excel, is_admin

class ExportUserData(BaseClassAction):
    def __init__(self, step_conversation, callback_data):
        super().__init__(step_conversation=step_conversation,
                         callback_data=callback_data)
        
        
    def on_conv_step(self, steps : dict):
        pass
    
    def create_handlers(self, application : Application, cancel):
        self.cancel = cancel

        states = {}
        states = self.on_conv_step(states)

        application.add_handler(CallbackQueryHandler(self.on_query_receive, pattern=self.callback_pattern))

    def on_menu_generate(self, keys : list):
        wallet_key = [InlineKeyboardButton("Export User Data", callback_data=self.callback_data)]
        
        keys.append(wallet_key)
        return keys

    async def on_query_receive(self,update: Update, context: CallbackContext):
        query = update.callback_query
        
        await query.edit_message_text("Exporting User Data...")
        
        users = []  # Get your user data here
    
        with db.session_scope() as session:
            users = session.query(User).all()
            
        export_to_excel(users)
        await query.edit_message_text("User data exported to Excel.")
        
        return ConversationHandler.END

        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass