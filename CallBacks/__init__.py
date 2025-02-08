from .SetWallet import SetWallet
from .ExportUserData import ExportUserData
from .SendToAll import SendToAll
from .UserProfile import UserProfile
from .BuyChance import BuyChance
from .GetTransactions import GetTransactions
from .StartNewLottery import StartNewLottery
from .GetCurrentLottery import GetCurrentLottery

userData = ExportUserData(1, "export_user_data")
wallet = SetWallet(2,"set_wallet")
sendToAll = SendToAll(3, "send_to_all")
userProfile = UserProfile(4, "user_profile")
buyChance = BuyChance(5, "buy_chance")
getTransactions = GetTransactions(6, "get_transactions")
startLottery = StartNewLottery(7, "start_new_lottery")
getCurrentLottery = GetCurrentLottery(8, "get_upcoming_lottery")