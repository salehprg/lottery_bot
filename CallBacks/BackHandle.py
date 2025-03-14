from datetime import datetime
import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from telegram.constants import ParseMode
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters,Application,CallbackQueryHandler,ConversationHandler
from Database import db, Settings
from Database.database import Lottery, LotteryUser, User
from sqlalchemy import func

class BackHandle(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)

    async def on_receive_input(self):
        """Handle the received input"""
        pass

    async def on_query_receive(self, update: Update, context: CallbackContext):
        
        await self.show_menu(update, context)
        return ConversationHandler.END
    