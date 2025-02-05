import datetime
import requests
import time
from Database import db, Settings, Transaction, Wallet
from typing import List

# Configuration
TRONSCAN_API_URL = "https://shastapi.tronscan.org/api/trx/transfer"
# YOUR_WALLET_ADDRESS = "TTcv9QtuHSYsEJpLbL7M4uCbsWBoW8ZkzY"  # Replace with your Tron wallet address

class TRX_TronScan:
    def __init__(self):
        pass

    def get_last_timestamp(self, session):
        settings = session.query(Settings).one()
        session.refresh(settings)

        return settings

    def start_pulling(self):
        print("Starting Tron payment system...")
        while True:
            try:
                session = db.SessionLocal()
                settings = self.get_last_timestamp(session)
                print("Polling for new transactions...")
                transactions = self.fetch_transactions(settings.lastTimeStampPull, settings.walletAddress)
                if transactions:
                    settings, new_transactions = self.process_transactions(transactions, settings)

                    old_settings = session.query(Settings).one()
                    old_settings.lastTimeStampPull = settings.lastTimeStampPull

                    for transaction in new_transactions:
                        user_wallet = session.query(Wallet).filter_by(current_walletaddress=f"{transaction.from_wallet}").one_or_none()
                        if user_wallet:
                            transaction.walletId = user_wallet.id
                            user_wallet.balance += transaction.amount

                        session.add(transaction)
                    else:
                        print("No new transactions found.")

                    session.commit()
            except Exception as ex:
                print(ex)

            time.sleep(5)

    def fetch_transactions(self, last_timestamp, wallet_address):
        params = {
            "sort": "-timestamp",  # Sort by latest transactions first
            "count": "true",       # Include total count of transactions
            "limit": 50,           # Fetch up to 20 transactions per request
            "start": 0,            # Start from the first transaction
            "address": wallet_address,
            "filterTokenValue": 0,  # Filter only TRX transfers (not tokens)
            "start_timestamp" : last_timestamp + 10
        }

        try:
            response = requests.get(TRONSCAN_API_URL, params=params)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching transactions: {e}")
            return []

    # Function to process transactions
    def process_transactions(self, transactions, settings : Settings) -> tuple[Settings, List[Transaction]]:

        LAST_TIMESTAMP = settings.lastTimeStampPull
        newset_timestamp = LAST_TIMESTAMP

        new_transactions = []
        for tx in transactions:
            tx_timestamp = tx.get("timestamp", LAST_TIMESTAMP)

            if tx.get("confirmed") == False or tx_timestamp <= LAST_TIMESTAMP:
                continue

            if tx_timestamp > newset_timestamp:
                newset_timestamp = tx_timestamp

            if tx.get("transferToAddress") == settings.walletAddress and tx.get("tokenInfo").get("tokenId") == "_":
                amount = tx.get("amount", 0) / 1_000_000  # Convert from sun to TRX
                # memo = tx.get("data", "")
                # memo_text = bytes.fromhex(memo).decode("utf-8") if memo else ""

                from_address = tx.get("transferFromAddress")
                # Extract user ID from memo (assuming memo format is "user_12345")
                # if memo_text.startswith("user_"):
                # user_id = memo_text.split("_")[1]

                transaction = Transaction()
                transaction.amount = amount
                transaction.from_wallet = from_address
                transaction.to_wallet = settings.walletAddress
                transaction.transactionDate = datetime.datetime.now()
                transaction.txn_id = tx.get("transactionHash")

                new_transactions.append(transaction)         

        settings.lastTimeStampPull = newset_timestamp
        print(f"New transactions {len(new_transactions)}")

        return settings, new_transactions