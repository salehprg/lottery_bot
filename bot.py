# bot.py
from multiprocessing import Process
import os
import threading
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler,CallbackContext, CallbackQueryHandler, Application,CommandHandler
from CallBacks import *
from handlers import show_menu, start
from Config import Configs
from Database import db, Settings
from apscheduler.schedulers.background import BackgroundScheduler
from Scheduler.LotteryScheduler import check_lottery

async def cancel(update: Update, context: ContextTypes) -> int:
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
    startLottery.create_handlers(application, cancel)
    getCurrentLottery.create_handlers(application, cancel)
    chooseLang.create_handlers(application, cancel)
    viewLotteryResult.create_handlers(application, cancel)
    inviteFriend.create_handlers(application, cancel)
    backHandle.create_handlers(application, cancel)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_menu))


    scheduler = BackgroundScheduler()
    # Schedule the job to run every 5 minutes using a cron expression.
    scheduler.add_job(check_lottery, 'cron', minute='*/5', args=[application])
    scheduler.start()

    print("Bot Started !")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()