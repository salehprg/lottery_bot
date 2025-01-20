# utils.py
import pandas as pd

def is_admin(user_id, admin_id):
    return user_id == admin_id

def export_to_excel(users):
    df = pd.DataFrame(users)
    df.to_excel("user_data.xlsx", index=False)
