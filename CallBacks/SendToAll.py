import re
from telegram import CallbackQuery, InlineKeyboardButton, Update, ReplyKeyboardRemove
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
        
        self.agree_step = int(f"{self.step_conversation}1")

    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
        
        steps[self.agree_step] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_agree),
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
        await update.message.chat.send_message("Enter your Message:", reply_markup=self.back_reply)
        
        return self.agree_step
    
    async def on_receive_agree(self,update: Update, context: CallbackContext):
        message = update.message.text
        
        if message == self.back_text:
            await self.show_menu(update, context)
            return ConversationHandler.END
         
        context.user_data["send_all_message"] = message
        
        reply_message = (
            f"Type OK to Accept this message:\n\n"
            f"{message}"
        )
        await update.message.reply_text(reply_message)
        
        return self.step_conversation
    
    async def on_receive_input(self,update: Update, context: CallbackContext):
        if not Configs.is_admin(update.message.from_user.id):
            return
        
        users_telegramIds = []
        
        if update.message.text == "OK":
            
            message = context.user_data["send_all_message"]

            with db.session_scope() as session:
                users = session.query(User).all()
                users_telegramIds = [user.telegramId for user in users]
                
            await update.message.reply_text(f"Your Message:\n\n {message}")
            await update.message.reply_text("Sending To All ...")
            
            for telegramId in users_telegramIds:
                try:
                    await context.bot.send_message(chat_id=telegramId, text=message)
                except TelegramError as e:
                    print(f"Error sending message to {telegramId}: {e}")

        await self.show_menu(update, context)
        return ConversationHandler.END
        