from .SetWallet import SetWallet
from .ExportUserData import ExportUserData
from .SendToAll import SendToAll
from .UserProfile import UserProfile
from .BuyChance import BuyChance
from .GetTransactions import GetTransactions
from .StartNewLottery import StartNewLottery
from .GetCurrentLottery import GetCurrentLottery
from .ChangeLanguage import ChangeLanguage
from .ViewLotteryResult import ViewLotteryResult

user_text_lang = {
    "en": {"caption" : "📥 Export User Data"},
    "fa": {"caption" : "📥 خروجی اکسل"}
}

wallet_text_lang = {
    "en": {
        "caption" : "💳 Define/Change Wallet Address",
        "exist_wallet": "A wallet with this address already exists."
        },
    "fa": {
        "caption" : "💳 تعریف/تغییر آدرس کیف پول",
        "exist_wallet" : "کیف پول با این آدرس موجود است."
        }
}

send_to_all_text_lang = {
    "en": {"caption" : "📩 Send Message to All"},
    "fa": {"caption" : "📩 ارسال پیام به همه کاربران"}
}

user_profile_text_lang = {
    "en": {
        "caption" : "User Profile",
        "profile": "User ID: {user_id}\n"
                    "Wallet balance: {balance}\n"
                    "Wallet address: {wallet_address}\n"
        },

    "fa": {
        "caption" : "پروفایل کاربر",
        "profile" : "شماره کاربر: {user_id}\n"
                    "موجودی کیف پول: {balance}\n"
                    "شماره کیف پول: {wallet_address}\n"
        }
}

buy_chance_text_lang = {
    "en": {"caption" : "🎫 Buy Chance (1 Tether)",
           "buy_chance" : ("Welcome to the 'Buy Chance' section! ✨\n"
                            "Each chance is equivalent to 1 Tether (1 TTR). 💰\n"
                            "To participate in the next lottery 🎉, please enter the number of chances you wish to purchase, and you will be automatically entered into the drawing.\n"
                            "🎯 We wish you success and hope that luck is on your side!\n\n"
                            "Your current chance: {current_chance}\n"
                            "Your wallet balance: {wallet_balance}\n"),
            "succed_buy": ("✅ Your payment was successful!\n"
                           "You have entered the raffle with {chance_float} chances. 🎉 \n"
                           "We wish you good luck! 🍀 \n"
                           "Good luck, and remember: Luck is on your side! 🌟\n\n"
                           "Your total chances: {total_chance}"),
            "empty_wallet": ( "Please first define your wallet in the '💳 Define/Change Wallet Address' section.\n"
                             "Then proceed to purchase a chance.\n" )
            },

    "fa": {"caption" : "🎫 خرید شانس (1 تتر)",
           "buy_chance" : ("به بخش 'خرید شانس' خوش آمدید! ✨\n"
                            "هر شانس معادل 1 تتر (1 TTR) است. 💰\n"
                            "برای شرکت در قرعه‌کشی بعدی 🎉، لطفاً تعداد شانس‌هایی که می‌خواهید خریداری کنید را وارد کنید. و به طور خودکار وارد قرعه‌کشی خواهید شد. \n"
                            "🎯 آرزوی موفقیت داریم و امیدواریم شانس با شما باشد!\n\n"
                            "شانس فعلی شما: {current_chance}\n"
                            "موجودی کیف پول شما: {wallet_balance}\n"),
            "succed_buy" :("✅ پرداخت شما با موفقیت انجام شد!"
                            "شما به تعداد {chance_float} شانس وارد قرعه‌کشی شدید. 🎉 \n"
                            "آرزو می‌کنیم که شانس با شما باشد! 🍀  \n"
                            "موفق باشید و به یاد داشته باشید: شانس در کنار شماست! 🌟\n\n"
                            "مجموع تعداد شانس های شما: {total_chance}"),
            "empty_wallet" : (
                            "لطفا ابتدا کیف پول خود را از بخش '💳 تعریف/تغییر آدرس کیف پول' تعریف کنید.\n"
                            "و سپس اقدام به خرید شانس نمایید.\n"
                            )
           }
}

get_transactions_text_lang = {
    "en": {"caption" : "📜 Track Payment"},
    "fa": {"caption" : "📊 بررسی واریزی‌ها"}
}

start_lottery_text_lang = {
    "en": {"caption" : "🎉 Start New Lottery"},
    "fa": {"caption" : "🎉 انجام قرعه‌کشی زمان‌بندی شده"}
}

get_current_lottery_text_lang = {
    "en": {"caption" : "📅 Next Draw Time"},
    "fa": {"caption" : "📅 زمان قرعه‌کشی بعدی"}
}

choose_lang_text_lang = {
    "en": {"caption" : "🌐 Change Language", 
           "select_lang" : "🌍 Please select your language",
           "response_lang" : "✅ Language set to English!"
           },
    "fa": {"caption" : "🌐 تغییر زبان", 
           "select_lang" : "لطفاً زبان خود را انتخاب کنید",
           "response_lang" : "✅ زبان به فارسی تنظیم شد!"
           }
}

view_result = {
    "en": {"caption" : "🏆 Prizes & Winners"},
    "fa": {"caption" : "🏆 مشاهده نتایج قرعه کشی"}
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
viewLotteryResult = ViewLotteryResult(10, view_result)
