from telegram import CallbackQuery, InlineKeyboardButton, Update
from telegram.constants import ParseMode
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters
from telegram.error import TelegramError
from config import ADMIN_ID
from utils import is_admin
from Database import db, Settings

class BuyChance(BaseClassAction):
    def __init__(self, step_conversation, callback_data):
        super().__init__(step_conversation=step_conversation,
                         callback_data=callback_data)
        
    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
        
    def on_menu_generate(self, keys : list):
        keyboard = [InlineKeyboardButton("Buy Chance", callback_data=self.callback_data)]
        
        keys.append(keyboard)
        return keys

    async def on_query_receive(self, query : CallbackQuery, update: Update, context: CallbackContext):
        
        user_id = update.effective_user.id
        
        settings = None
        wallet = None
        profileinfo = ""
        
        with db.session_scope() as session:
            settings = session.query(Settings).one()

            profileinfo = f"""هر شانس معادل 1TRON میباشد لطفا مبلغ معادل را به کیف پول زیر واریز نمایید:\nکیف پول:`{settings.walletAddress}`"""

        await update.effective_chat.send_message(profileinfo, parse_mode=ParseMode.MARKDOWN_V2)
        
        return self.step_conversation
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass