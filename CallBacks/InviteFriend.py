import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, Application, CallbackQueryHandler, ConversationHandler
from telegram.error import TelegramError
from Domain.DTOs.UserDTO import UserDTO
from Database import db, User
from Config import Configs
from telegram.constants import ParseMode

class InviteFriend(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)

    async def on_query_receive(self,update: Update, context: CallbackContext):
        
        user_id = update.message.from_user.id
    
        invited_users_count = 0

        with db.session_scope() as session:
            invited_users_count = session.query(User).filter_by(inviteby_telegramId=f"{user_id}").count()

        invite_message = self.get_text(context, "InviteText").format(invite_user_count=invited_users_count, ref_code=user_id)

        await update.message.chat.send_message(invite_message, parse_mode=ParseMode.HTML)
        
        return ConversationHandler.END

        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass