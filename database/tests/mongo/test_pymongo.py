from datetime import date
from typing import cast

from mongo.pymongo import clear_all, create_user, find_user
from mongo.pymongo.pymongo import UserModel


def setup_function() -> None:
    clear_all()


def test_user_collection() -> None:
    create_user(
        cast(
            UserModel,
            {
                "name": "Alvin",
                "birthday": date(1981, 3, 17),
                "city": {
                    "name": "Xi'an",
                },
            },
        )
    )

    users = find_user(
        name="Alvin",
        birthday=date(1981, 3, 17),
    )
    assert users == [
        {
            "name": "Alvin",
            "birthday": date(1981, 3, 17),
            "city": {
                "country": "China",
                "name": "Xi'an",
            },
        },
    ]
