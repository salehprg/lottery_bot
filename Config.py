from Database import db, Settings

class Configs:
    save_path = ""
    TOKEN = "7809913716:AAGB4fCSrXa1pYjpNndWfW23vGOhmc6OF_A"

    @staticmethod
    def is_admin(user_id):
        
        admin_list = []
        with db.session_scope() as session:
            settings = session.query(Settings).one_or_none()
            if settings is not None:
                for adminId in settings.adminIds:
                    admin_list.append(adminId)

        return user_id in admin_list