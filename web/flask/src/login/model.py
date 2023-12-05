from typing import Dict, Optional

from flask_login import UserMixin

# 用户存储对象
_USER_STORE: Dict[int, "UserModel"] = {}


class UserModel(UserMixin):
    id: int
    name: str
    password: str
    email: str
    telephone: str

    @classmethod
    def create(
        cls, id: int, name: str, password: str, email: str, telephone: str
    ) -> "UserModel":
        user = cls(id, name, password, email, telephone)
        _USER_STORE[id] = user
        return user

    @classmethod
    def get(cls, id: int) -> "UserModel":
        return _USER_STORE[id]

    @classmethod
    def find_by_name(cls, name: str) -> Optional["UserModel"]:
        for user in _USER_STORE.values():
            if user.name == name:
                return user

        return None
