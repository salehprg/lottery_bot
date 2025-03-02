import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from telegram.constants import ParseMode
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters,Application,CallbackQueryHandler,ConversationHandler
from Database import db, Settings

class BuyChance(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        
    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]


    async def on_query_receive(self, update: Update, context: CallbackContext):
        
        user_id = update.effective_user.id
        
        settings = None
        wallet = None
        profileinfo = ""
        
        with db.session_scope() as session:
            settings = session.query(Settings).one()

            profileinfo = f"""هر شانس معادل 1TRON میباشد لطفا مبلغ معادل را به کیف پول زیر واریز نمایید:\n\nکیف پول: `{settings.walletAddress}`"""

        await update.message.chat.send_message(profileinfo, parse_mode=ParseMode.MARKDOWN_V2)
        
        if self.cancel is not None:
            return await self.cancel(update, context)
        
        return ConversationHandler.END
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass