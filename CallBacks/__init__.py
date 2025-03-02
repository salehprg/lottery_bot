from .SetWallet import SetWallet
from .ExportUserData import ExportUserData
from .SendToAll import SendToAll
from .UserProfile import UserProfile
from .BuyChance import BuyChance
from .GetTransactions import GetTransactions
from .StartNewLottery import StartNewLottery
from .GetCurrentLottery import GetCurrentLottery
from .ChangeLanguage import ChangeLanguage

user_text_lang = {
    "en": {"caption" : "Export User Data"},
    "fa": {"caption" : "📥 خروجی اکسل"}
}

wallet_text_lang = {
    "en": {"caption" : "Set Wallet"},
    "fa": {"caption" : "💳 تعریف/تغییر آدرس کیف پول"}
}

send_to_all_text_lang = {
    "en": {"caption" : "Send to All"},
    "fa": {"caption" : "📩 ارسال پیام به همه کاربران"}
}

user_profile_text_lang = {
    "en": {"caption" : "User Profile"},
    "fa": {"caption" : "پروفایل کاربر"}
}

buy_chance_text_lang = {
    "en": {"caption" : "Buy Chance"},
    "fa": {"caption" : "🎫 خرید شانس (1 تتر)"}
}

get_transactions_text_lang = {
    "en": {"caption" : "Get Transactions"},
    "fa": {"caption" : "📊 بررسی واریزی‌ها"}
}

start_lottery_text_lang = {
    "en": {"caption" : "Start New Lottery"},
    "fa": {"caption" : "🎉 انجام قرعه‌کشی زمان‌بندی شده"}
}

get_current_lottery_text_lang = {
    "en": {"caption" : "Get Upcoming Lottery"},
    "fa": {"caption" : "📅 زمان قرعه‌کشی بعدی"}
}

choose_lang_text_lang = {
    "en": {"caption" : "Change Language", 
           "select_lang" : "🌍 Please select your language",
           "response_lang" : "✅ Language set to English!"
           },
    "fa": {"caption" : "🌐 تغییر زبان", 
           "select_lang" : "لطفاً زبان خود را انتخاب کنید",
           "response_lang" : "✅ زبان به فارسی تنظیم شد!"
           }
}


# Creating objects with translated text
userData = ExportUserData(1, user_text_lang)
wallet = SetWallet(2, wallet_text_lang)
sendToAll = SendToAll(3, send_to_all_text_lang)
userProfile = UserProfile(4, user_profile_text_lang)
buyChance = BuyChance(5, buy_chance_text_lang)
getTransactions = GetTransactions(6, get_transactions_text_lang)
startLottery = StartNewLottery(7, start_lottery_text_lang)
getCurrentLottery = GetCurrentLottery(8, get_current_lottery_text_lang)
chooseLang = ChangeLanguage(9, choose_lang_text_lang)
