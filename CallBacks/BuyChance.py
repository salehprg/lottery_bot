from telegram import CallbackQuery, InlineKeyboardButton, Update
from telegram.constants import ParseMode
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters,Application,CallbackQueryHandler,ConversationHandler
from Database import db, Settings

class BuyChance(BaseClassAction):
    def __init__(self, step_conversation, callback_data):
        super().__init__(step_conversation=step_conversation,
                         callback_data=callback_data)
        
    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
    
    def create_handlers(self, application : Application, cancel):
        self.cancel = cancel

        states = {}
        self.on_conv_step(states)

        application.add_handler(CallbackQueryHandler(self.on_query_receive, pattern=self.callback_pattern))

    def on_menu_generate(self, keys : list):
        keyboard = [InlineKeyboardButton("Buy Chance", callback_data=self.callback_data)]
        
        keys.append(keyboard)
        return keys

    async def on_query_receive(self, update: Update, context: CallbackContext):
        
        user_id = update.effective_user.id
        
        settings = None
        wallet = None
        profileinfo = ""
        
        with db.session_scope() as session:
            settings = session.query(Settings).one()

            profileinfo = f"""هر شانس معادل 1TRON میباشد لطفا مبلغ معادل را به کیف پول زیر واریز نمایید:\n\nکیف پول: `{settings.walletAddress}`"""

        await update.callback_query.edit_message_text(profileinfo, parse_mode=ParseMode.MARKDOWN_V2)
        
        if self.cancel is not None:
            return await self.cancel(update, context)
        
        return ConversationHandler.END
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass