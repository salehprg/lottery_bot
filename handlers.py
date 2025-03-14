from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from Config import Configs
from Database.database import db,User, Wallet
from CallBacks import *

async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    
    with db.session_scope() as session:
        exist_user = session.query(User).filter_by(telegramId=f"{user_id}").one_or_none()
        if exist_user == None:
            refered_userId = ""
            
            referred_by = update.message.text.split('/start ')
            if len(referred_by) > 1:
                refered_userId = referred_by[1]
        
            new_user = User()
            new_user.telegramId = f"{user_id}"
            new_user.telegramUsername = username
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
    if Configs.is_admin(user_id):
        await admin_panel(update, context)
    else:
        await user_panel(update, context)
        
async def user_panel(update: Update, context: CallbackContext):

    keyboard =[]
    

    prof_btn = userProfile.on_menu_generate(context)[0]
    wallet_btn = wallet.on_menu_generate(context)[0]
    user_section = [prof_btn, wallet_btn]
    keyboard.append(user_section)

    buycahnce_btn = buyChance.on_menu_generate(context)[0]
    lottery_result_btn = viewLotteryResult.on_menu_generate(context)[0]
    lottery_section = [buycahnce_btn, lottery_result_btn]
    keyboard.append(lottery_section)

    keyboard.append(getCurrentLottery.on_menu_generate(context))

    lang = chooseLang.on_menu_generate(context)[0]
    invite = inviteFriend.on_menu_generate(context)[0]
    social_section = [lang, invite]
    keyboard.append(social_section)
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    if update.callback_query:
        await update.callback_query.message.chat.send_message("Welcome to the User Panel. Choose an action:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Welcome to the User Panel. Choose an action:", reply_markup=reply_markup)

async def admin_panel(update: Update, context: CallbackContext):
    keyboard = []
    
    excel = userData.on_menu_generate(context)[0]
    setWallet = wallet.on_menu_generate(context)[0]
    user_section = [excel, setWallet]
    keyboard.append(user_section)

    keyboard.append(sendToAll.on_menu_generate(context))
    keyboard.append(getTransactions.on_menu_generate(context))

    lottery = startLottery.on_menu_generate(context)[0]
    currentLottery = getCurrentLottery.on_menu_generate(context)[0]
    social_section = [lottery, currentLottery]
    keyboard.append(social_section)
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    message = update.callback_query if update.callback_query is not None else update.message
    
    if update.callback_query:
        await update.callback_query.message.chat.send_message("Welcome to the Admin Panel. Choose an action:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Welcome to the Admin Panel. Choose an action:", reply_markup=reply_markup)


backHandle.show_menu_func = show_menu
chooseLang.show_menu_func = show_menu
sendToAll.show_menu_func = show_menu
wallet.show_menu_func = show_menu
startLottery.show_menu_func = show_menu