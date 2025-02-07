from abc import ABC, abstractmethod

from telegram import CallbackQuery, Update
from telegram.ext import CallbackContext, Application

class BaseClassAction(ABC):

    def __init__(self, step_conversation, callback_data):
        super().__init__()
        self.step_conversation = step_conversation
        self.callback_data = callback_data
        self.cancel = None
        self.callback_pattern = "^" + self.callback_data + "$"

    @abstractmethod
    def on_conv_step(self, steps : dict):
        pass

    @abstractmethod
    def create_handlers(self, application : Application, cancel):
        pass
    
    @abstractmethod
    def on_menu_generate(self) -> list:
        """Handle the menu generation logic"""
        pass

    async def on_query_receive(self, query : CallbackQuery,update: Update, context: CallbackContext):
        """Handle the received query"""
        pass

    @abstractmethod
    async def on_receive_input(self):
        """Handle the received input"""
        pass
