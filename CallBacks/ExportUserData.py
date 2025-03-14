from datetime import datetime
import os
import re
import pandas as pd
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters,Application,CallbackQueryHandler
from Database.database import db,User
from Domain.DTOs.UserDTO import UserDTO
from Domain.mapper import map_to_dto
from Config import Configs

class ExportUserData(BaseClassAction):
    def __init__(self, step_conversation, text_translates):
        super().__init__(step_conversation=step_conversation,
                         text_translates=text_translates)
        

    async def on_query_receive(self,update: Update, context: CallbackContext):

        await update.message.chat.send_message("Exporting User Data...")
        
        users_dto = []  # Get your user data here
    
        with db.session_scope() as session:
            users = session.query(User).all()

            for transaction in users:
                dto = map_to_dto(transaction, UserDTO)
                users_dto.append(dto)
        
        data = {
            "ID": [t.id for t in users_dto],
            "Telegram ID": [t.telegramId for t in users_dto],
            "Telegram Username": [t.telegramUsername for t in users_dto],
            "Invite By ID": [t.inviteby_telegramId for t in users_dto],
            "Join Date": [t.joinDate for t in users_dto]
        }

        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        file_path = os.path.join(Configs.save_path, f"UserData_{timestamp}.xlsx")

        df.to_excel(file_path, index=False)

        result_text = f"""Users information:\nTotal: {len(users_dto)}\n"""

        await update.message.chat.send_message(result_text)

        with open(file_path, "rb") as file:
            await update.message.chat.send_document(file, caption="Users file")
        
        return ConversationHandler.END

        
    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass