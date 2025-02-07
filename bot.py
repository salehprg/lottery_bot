# bot.py
from multiprocessing import Process
import os
import threading
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler,CallbackContext, CallbackQueryHandler, Application,CommandHandler
from TRX_TronScan import TRX_TronScan
from CallBacks import *
from handlers import show_menu, start
from Config import Configs


async def cancel(update: Update, context: ContextTypes) -> int:

    await show_menu(update, context)
    return ConversationHandler.END
    
def main():
    
    save_path = os.getenv("SAVE_DIR_PATH", "./data")
    os.makedirs(save_path,exist_ok=True)

    Configs.save_path = save_path
    
    print("Starting...")
    application = Application.builder().token(Configs.TOKEN).build()
    
    # application.add_handler(conv_handler)
    # Command Handlers

    wallet.create_handlers(application, cancel)
    userProfile.create_handlers(application, cancel)
    sendToAll.create_handlers(application, cancel)
    buyChance.create_handlers(application, cancel)
    getTransactions.create_handlers(application, cancel)
    userData.create_handlers(application, cancel)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_menu))

    print("Bot Started !")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

def start_pulling_trx():
    trx_payment = TRX_TronScan()
    trx_payment.start_pulling()

if __name__ == "__main__":
    
    p = Process(target=start_pulling_trx)
    p.start()

    while True:
        try:
            main()
        except Exception as ex:
            print(ex)

    p.join()