# bot.py
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler,CallbackContext, CallbackQueryHandler, Application,CommandHandler
from config import TOKEN
from CallBacks import *
from handlers import show_menu, start

callbacks = {
    wallet.callback_data : wallet,
    userData.callback_data : userData,
    sendToAll.callback_data : sendToAll,
    userProfile.callback_data : userProfile,
    buyChance.callback_data : buyChance,
}

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

    return ConversationHandler.END

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    action = callbacks[query.data]
    if action:
        return await action.on_query_receive(query, update, context)
    
    # if query.data == "buy_ticket":
    #     await query.edit_message_text("You bought a lottery ticket!")
    # elif query.data == "invite":
    #     await query.edit_message_text("You can invite friends using the invite link!")
    # elif query.data == "check_time":
    #     await query.edit_message_text("The draw will happen in X minutes.")
    # elif query.data == "send_message":
    #     await query.edit_message_text("You can send a message to all users here.")
    # elif query.data == userData.callback_data:
    #     return await userData.on_query_receive(query)
    # elif query.data == wallet.callback_data:
    #     return await wallet.on_query_receive(query)
    
def main():
    
    states = {}
    
    wallet.on_conv_step(states)
    userData.on_conv_step(states)
    sendToAll.on_conv_step(states)
    userProfile.on_conv_step(states)
    buyChance.on_conv_step(states)
    
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],  # The conversation is triggered by the inline button, not a direct command
        states=states,
        fallbacks=[CommandHandler("cancel", cancel)],
    )
        
    print("Starting...")
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(conv_handler)
    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_menu))
    # application.add_handler(CommandHandler(AdminPanel.command, AdminPanel.function))
    # application.add_handler(CommandHandler(SendToAll.command, SendToAll.function))
    # application.add_handler(CommandHandler(ExportData.command, ExportData.function))
    # application.add_handler(CommandHandler(SetWalletAddress.command, SetWalletAddress.function))
    
    
    print("Bot Started !")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
