from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from config import ADMIN_ID
from utils import is_admin, export_to_excel
from Database.database import db,User, Wallet
from CallBacks import *
                    
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    with db.session_scope() as session:
        exist_user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
        if exist_user == None:
            refered_userId = ""
            
            referred_by = update.message.text.split('/start ')
            if len(referred_by) > 1:
                refered_userId = referred_by[1]
        
            new_user = User()
            new_user.telegramId = f"{user_id}"
            new_user.inviteby_telegramId = refered_userId
            session.add(new_user)
            session.flush()
            
            new_wallet = Wallet()
            new_wallet.balance = 0
            new_wallet.userId = new_user.id
            session.add(new_wallet)

    await show_menu(update, context)
            
    

async def show_menu(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if is_admin(user_id, ADMIN_ID):
        await admin_panel(update, context)
    else:
        await user_panel(update, context)
        
async def user_panel(update: Update, context: CallbackContext):
    # keyboard = [
    #     [InlineKeyboardButton("Buy Lottery Ticket", callback_data=BUY_TICKET)],
    #     [InlineKeyboardButton("Invite Friends", callback_data=INVITE),
    #     InlineKeyboardButton("Check Remaining Time", callback_data=CHECK_TIME)],
    # ]
    
    keyboard =[]
    
    userProfile.on_menu_generate(keyboard)
    wallet.on_menu_generate(keyboard)
    buyChance.on_menu_generate(keyboard)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.message.chat.send_message("Welcome to the User Panel. Choose an action:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Welcome to the User Panel. Choose an action:", reply_markup=reply_markup)

async def admin_panel(update: Update, context: CallbackContext):
    keyboard = []
    
    userData.on_menu_generate(keyboard)
    wallet.on_menu_generate(keyboard)
    sendToAll.on_menu_generate(keyboard)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.callback_query if update.callback_query is not None else update.message

    await message.reply_text("Welcome to the Admin Panel. Choose an action:", reply_markup=reply_markup)