from Database import db, Settings

class Configs:
    save_path = ""
    TOKEN = "7648992316:AAHHGWLxM3zi7bpYG9tS0W-W_27blSy6yxk"

    @staticmethod
    def is_admin(user_id):
        
        admin_list = []
        with db.session_scope() as session:
            settings = session.query(Settings).one_or_none()
            if settings is not None:
                for adminId in settings.adminIds:
                    admin_list.append(adminId)

        return user_id in admin_list