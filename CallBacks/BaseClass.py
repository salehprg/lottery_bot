from abc import ABC, abstractmethod
import re

from telegram import CallbackQuery, InlineKeyboardButton, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Application, MessageHandler, filters

class BaseClassAction(ABC):

    def __init__(self, step_conversation, text_translates : dict):
        super().__init__()
        self.step_conversation = step_conversation
        self.text_translates = text_translates
        self.cancel = None
        self.show_menu_func = None

        self.back_text = "⬅️"
        self.back_reply = ReplyKeyboardMarkup(keyboard=[[InlineKeyboardButton(self.back_text)]], resize_keyboard=True, one_time_keyboard=False)

    async def show_menu(self, update, context):
        if self.show_menu_func is not None:
            await self.show_menu_func(update, context)

    def get_text(self, context, key : str = 'caption'):
        lang = context.user_data.get("lang", "en")
        
        if lang in self.text_translates.keys():
            return self.text_translates[lang][key]
        
        return self.text_translates['en'][key]
    
    def get_regex_pattern(self):
        # Extract all translation values
        all_translations = []
        for lang in self.text_translates:
            for val in self.text_translates[lang].keys():
                if val == "caption":
                    all_translations.append(self.text_translates[lang][val])
                
        regex_pattern = f"^({'|'.join(map(re.escape, all_translations))})$"
        
        return regex_pattern
    
    def on_conv_step(self, steps : dict):
        pass

    def create_handlers(self, application : Application, cancel):
        self.cancel = cancel
        regex_pattern = self.get_regex_pattern()
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(regex_pattern), self.on_query_receive))
        

    def on_menu_generate(self, context : CallbackContext):
        text = self.get_text(context)
        buttons = [InlineKeyboardButton(text, callback_data=self.step_conversation)]
        
        return buttons

    async def on_query_receive(self, query : CallbackQuery,update: Update, context: CallbackContext):
        """Handle the received query"""
        pass

    @abstractmethod
    async def on_receive_input(self):
        """Handle the received input"""
        pass
