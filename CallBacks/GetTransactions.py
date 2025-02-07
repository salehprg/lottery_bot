from datetime import datetime
import os
import pandas as pd
from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, ContextTypes, Application

from Database.database import Wallet
from Domain.DTOs.TransactionsDTO import TransactionDTO
from Domain.mapper import map_to_dto

from Config import Configs
from Database import db, Settings, Transaction

class GetTransactions(BaseClassAction):
    def __init__(self, step_conversation, callback_data):
        super().__init__(step_conversation=step_conversation,
                         callback_data=callback_data)

        self.agree_step = int(f"{self.step_conversation}1")
    
    def create_handlers(self, application : Application, cancel):
        self.cancel = cancel

        application.add_handler(CallbackQueryHandler(self.on_query_receive, pattern=self.callback_pattern))
        
    def on_conv_step(self, steps : dict):
        pass
        
    def on_menu_generate(self, keys : list):
        wallet_key = [InlineKeyboardButton("Get Users Transactions", callback_data=self.callback_data)]
        
        keys.append(wallet_key)
        return keys

    async def on_query_receive(self,update: Update, context: CallbackContext):
        
        transactions_dto = []
        total_amount = 0
        unique_wallets = set()
    
        with db.session_scope() as session:
            transactions = session.query(Transaction).all()
            for transaction in transactions:
                dto = map_to_dto(transaction, TransactionDTO)
                transactions_dto.append(dto)

                total_amount += dto.amount
                unique_wallets.add(dto.from_wallet)

        data = {
            "ID": [t.id for t in transactions_dto],
            "Transaction ID": [t.txn_id for t in transactions_dto],
            "From Wallet": [t.from_wallet for t in transactions_dto],
            "Amount": [t.amount for t in transactions_dto],
            "Transaction Date": [t.transactionDate for t in transactions_dto]
        }

        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        file_path = os.path.join(Configs.save_path, f"transactions_{timestamp}.xlsx")

        df.to_excel(file_path, index=False)
        
        result_text = f"""Transactions information:\nTotal: {len(transactions_dto)}\nAmount: {total_amount}\nUnique Wallets: {len(unique_wallets)}"""

        await update.callback_query.edit_message_text(result_text)

        with open(file_path, "rb") as file:
            await update.callback_query.message.chat.send_document(file, caption="Transaction file")

        return self.agree_step

    async def on_receive_input(self,update: Update, context: CallbackContext):
        pass