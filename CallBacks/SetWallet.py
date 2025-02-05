from telegram import CallbackQuery, InlineKeyboardButton, Update
from CallBacks.BaseClass import BaseClassAction
from telegram.ext import CallbackContext, MessageHandler, filters

from Database.database import Wallet
from config import ADMIN_ID
from utils import is_admin

from Database import db, Settings, User

class SetWallet(BaseClassAction):
    def __init__(self, step_conversation, callback_data):
        super().__init__(step_conversation=step_conversation,
                         callback_data=callback_data)
        
        self.agree_step = int(f"{self.step_conversation}1")
        
    def on_conv_step(self, steps : dict):
        steps[self.step_conversation] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_input),
            ]
        
        steps[self.agree_step] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_receive_agree),
            ]
        return steps
        
    def on_menu_generate(self, keys : list):
        wallet_key = [InlineKeyboardButton("Set Wallet Address", callback_data=self.callback_data)]
        
        keys.append(wallet_key)
        return keys

    async def on_query_receive(self, query : CallbackQuery,update: Update, context: CallbackContext):
        await query.edit_message_text("Enter your wallet Address:")
        
        return self.agree_step

    async def on_receive_agree(self,update: Update, context: CallbackContext):
        # if not is_admin(update.message.from_user.id, ADMIN_ID):
        #     return

        new_wallet_address = update.message.text
        
        context.user_data["wallet"] = new_wallet_address
        
        await update.message.reply_text(f"Type OK to Update Wallet Address: {new_wallet_address}")
        
        return self.step_conversation
        
    async def on_receive_input(self,update: Update, context: CallbackContext):       
        user_data = context.user_data
        user_id = update.effective_user.id

        new_wallet_address = user_data["wallet"]
        
        if update.message.text == "OK":
            
            with db.session_scope() as session:

                if not is_admin(update.message.from_user.id, ADMIN_ID):
                    user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
                    if user != None:
                        wallet = session.query(Wallet).filter_by(userId=user.id).one_or_none()
                        wallet.current_walletaddress = new_wallet_address
                else:
                    settings = session.query(Settings).one()
                    settings.walletAddress = new_wallet_address
            
            await update.message.reply_text(f"Wallet address updated to {new_wallet_address}")