from flask_login import UserMixin


_user_list = {
    1: []
}


class User(UserMixin):
    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def get_id(self):
        return 0
