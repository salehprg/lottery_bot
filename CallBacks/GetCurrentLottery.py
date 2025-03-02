from datetime import datetime
import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, ContextTypes, Application
from telegram.constants import ParseMode
from Database.database import Wallet

from Database import db, Lottery
from Config import Configs

class GetCurrentLottery(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        

    async def on_query_receive(self,update: Update, context: CallbackContext):
        
        user_id = update.effective_user.id

        lottery_date = None
        with db.session_scope() as session:
            lottery = session.query(Lottery).filter(Lottery.startDate > datetime.now()).order_by(Lottery.startDate).first()
            if lottery is not None:
                lottery_date = lottery.startDate

        if lottery_date is not None:
            await update.message.chat.send_message(f"Upcoming Lottery:\n\n*{lottery_date.strftime('%Y/%m/%d %H:%M')}*", parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await update.message.chat.send_message(f"Currently there isnt any Lottery!")
        
        await self.cancel(update, context)

    async def on_receive_input(self,update: Update, context: CallbackContext):       
        pass