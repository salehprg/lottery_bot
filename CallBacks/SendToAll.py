import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, Application, CallbackQueryHandler, ConversationHandler
from telegram.error import TelegramError
from Domain.DTOs.UserDTO import UserDTO
from Database import db, User
from Config import Configs

class SendToAll(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        
    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]

        return steps
    
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
    

    async def on_query_receive(self,update: Update, context: CallbackContext):
        await update.message.chat.send_message("Enter your Message:")
        
        return self.step_conversation
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        if not Configs.is_admin(update.message.from_user.id):
            return
        
        users_dto = []
    
        with db.session_scope() as session:
            users = session.query(User).all()
            users_dto = [UserDTO(user.id, user.telegramId, user.inviteby_telegramId, user.joinDate) for user in users]
            
        message = update.message.text
        await update.message.reply_text(f"Your Message: \n{message}")
        sending = await update.message.reply_text("Sending To All ...")
        
        for user in users_dto:
            user_id = user.telegramId
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
            except TelegramError as e:
                print(f"Error sending message to {user_id}: {e}")