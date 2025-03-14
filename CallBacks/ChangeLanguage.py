import re
from telegram import CallbackQuery, InlineKeyboardButton, ReplyKeyboardMarkup, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, Application, ConversationHandler, CallbackQueryHandler
from Database import db, User,Wallet

class ChangeLanguage(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        
        self.CHOOSE_LANGUAGE = 1
    
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
        
    def on_conv_step(self, steps : dict):
        steps[self.CHOOSE_LANGUAGE] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
        return steps

    async def on_query_receive(self, update: Update, context: CallbackContext):
        keyboard = [["English", "فارسی"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        reply_text = self.get_text(context, "select_lang")
        await update.message.reply_text(
            reply_text,
            reply_markup=reply_markup
        )
        
        return self.CHOOSE_LANGUAGE
        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        selected_language = update.message.text

        if selected_language == "English":
            context.user_data["lang"] = "en"
        elif selected_language == "فارسی":
            context.user_data["lang"] = "fa"
        else:
            await update.message.reply_text("❌ Invalid choice! Please select again.")
            return self.CHOOSE_LANGUAGE

        reply_text = self.get_text(context, "response_lang")
        await update.message.reply_text(reply_text)
        
        await self.show_menu(update, context)
            
        return ConversationHandler.END