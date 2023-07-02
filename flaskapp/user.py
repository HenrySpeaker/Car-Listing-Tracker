from db.dbi.db_interface import DBInterface
from flask_login import UserMixin


class User(UserMixin):  # pragma: no cover
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username

    def get_id(self):
        return str(self.user_id)
