from datetime import datetime
import random
import uuid
from sqlalchemy import func
from Database import db, Settings
from Database.database import Lottery, LotteryUser

# Assume these are your SQLAlchemy models and session
# from models import Lottery, LotteryUser
# from database import session

def check_lottery():
    with db.session_scope() as session:
        lottery = session.query(Lottery)\
            .filter(Lottery.startDate < datetime.now())\
            .order_by(Lottery.startDate.desc(), Lottery.winnerId != None).first()
        
        if lottery is None:
            print("No upcoming lottery found.")
            return
        
        # Check if the lottery start date has passed
        if lottery.startDate > datetime.now():
            print("Lottery start date has not been reached yet.")
            return

        # Fetch all records for the current lottery from LotteryUser
        lottery_users = session.query(LotteryUser)\
            .filter_by(lotteryId=str(lottery.id))\
            .all()

        # Create a dictionary: user_id -> total ticket amount (chance)
        user_amounts = {}
        for lu in lottery_users:
            user_id = lu.userId
            # Only calculate if not already computed
            if user_id not in user_amounts:
                total_amount = session.query(func.sum(LotteryUser.ticketAmount))\
                    .filter_by(userId=user_id, lotteryId=str(lottery.id))\
                    .scalar() or 0
                user_amounts[user_id] = total_amount

        if not user_amounts:
            winner = uuid.UUID(int=0)
            lottery.winnerId = winner
            lottery.poolSize = 0
            lottery.userCount = 0
            
            return

        # Prepare lists for weighted selection
        user_ids = list(user_amounts.keys())
        weights = list(user_amounts.values())

        winner = random.choices(user_ids, weights=weights, k=1)[0]

        lottery.winnerId = winner
        lottery.poolSize = sum(weights)
        lottery.userCount = len(user_ids)

        print("Lottery winner is:", winner)