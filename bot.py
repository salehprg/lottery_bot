# bot.py
import threading
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler,CallbackContext, CallbackQueryHandler, Application,CommandHandler
from TRX_TronScan import TRX_TronScan
from config import TOKEN
from CallBacks import *
from handlers import show_menu, start

callbacks = {
    userData.callback_data : userData,
    sendToAll.callback_data : sendToAll,
    userProfile.callback_data : userProfile,
    buyChance.callback_data : buyChance,
}

async def cancel(update: Update, context: ContextTypes) -> int:

    await show_menu(update, context)
    return ConversationHandler.END

async def button(update: Update, context: CallbackContext):
    query = update.callback_query

    await query.answer()

    print("Query Received")

    action = callbacks[query.data]
    if action:
        conv_step = await action.on_query_receive(query, update, context)
        return conv_step
    
def main():
            
    print("Starting...")
    application = Application.builder().token(TOKEN).build()
    
    # application.add_handler(conv_handler)
    # Command Handlers

    wallet.create_handlers(application, cancel)
    userProfile.create_handlers(application, cancel)
    sendToAll.create_handlers(application, cancel)
    buyChance.create_handlers(application, cancel)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_menu))

    
    print("Bot Started !")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    trx_payment = TRX_TronScan()
    scheduler_tron = threading.Thread(target=trx_payment.start_pulling)
    scheduler_tron.start()

    while True:
        try:
            main()
        except Exception as ex:
            print(ex)

    scheduler_tron.join()