from Models.user import User
from Controllers.context_manager import ContextManager

class UserController:
    def __init__(self):
        self.db = ContextManager()

    def get_user(self, user_id):
        raw_student = self.db.execute(
            "SELECT first_name, last_name, id FROM users WHERE id = ?",
            (1, ),
            fetch_mode='one'
        )

        if raw_student:
            return {
                'success': True,
                'user': User(*raw_student[:2], identifier=raw_student[2])
            }

        return {
            'success': False,
            'message': "User not found!"
        }
