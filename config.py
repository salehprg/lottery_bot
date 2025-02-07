# utils.py
import os
import pandas as pd

class Configs:
    save_path = ""
    ADMIN_ID = 107948594
    TOKEN = "7809913716:AAHboDUMKA3hyEeMKLryIuNKIU_KR3s5ihk"

    @staticmethod
    def is_admin(user_id, admin_id):
        return user_id == admin_id