from datetime import datetime
import re
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, ContextTypes, Application
from telegram.constants import ParseMode
from Database.database import Wallet

from Database import db, Lottery
from Config import Configs

class StartNewLottery(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        
        self.agree_step = int(f"{self.step_conversation}1")
    
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
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
        
        steps[self.agree_step] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_agree),
            ]
        return steps


    async def on_query_receive(self,update: Update, context: CallbackContext):

        lottery_date = None
        with db.session_scope() as session:
            lottery = session.query(Lottery).filter(Lottery.startDate > datetime.now()).order_by(Lottery.startDate).first()
            if lottery is not None:
                lottery_date = lottery.startDate
        
        if lottery_date is None:
            await update.message.chat.send_message("""Enter new Lottery Date:\nPlease use this format: *YYYY/MM/DD hh:mm*\nYYYY: Year\nMM: Month\nDD: Day\nhh: Hour\nmm: Minute""", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=self.back_reply)
            return self.step_conversation
        else:
            await update.message.chat.send_message("Currently you have an upcoming lottery!\nYou cant add new lottery")
            return ConversationHandler.END
        

    async def on_receive_agree(self,update: Update, context: CallbackContext):
        
        message = update.message.text
        
        lottery_date = context.user_data["lottery_date"]
        datetime_object = datetime.strptime(lottery_date, "%Y/%m/%d %H:%M")

        if message == "OK":
            with db.session_scope() as session:
                new_lottery = Lottery()
                new_lottery.startDate = datetime_object
                new_lottery.poolSize = 0
                new_lottery.userCount = 0

                session.add(new_lottery)

        await update.message.reply_text(f"Lottery Created !")
        
        await self.show_menu(update, context)
        return ConversationHandler.END
    
    def is_valid_format(self, input_string):
        # Regular expression to match the format yyyy/mm/dd hh:mm
        pattern = r"^\d{4}/\d{2}/\d{2} \d{2}:\d{2}$"
        return re.match(pattern, input_string) is not None

    async def on_receive_input(self,update: Update, context: CallbackContext):       
        
        message = update.message.text

        if message == self.back_text:
            await self.show_menu(update, context)
            return ConversationHandler.END

        if self.is_valid_format(message):
            context.user_data["lottery_date"] = message

            await update.message.reply_text(f"Type OK to Create new lottery for entered date:\n{message}")
            return self.agree_step
        else:
            await update.message.reply_text(f"Enter in correct format please:\nyyyy/mm/dd hh:mm")
            return self.step_conversation