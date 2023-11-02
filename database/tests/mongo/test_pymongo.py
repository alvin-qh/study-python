from datetime import date

from mongo.pymongo import clear_all, create_user, find_user


def setup_function() -> None:
    clear_all()


def test_user_collection() -> None:
    create_user(
        {
            "name": "Alvin",
            "birthday": date(1981, 3, 17),
            "city": {
                "name": "Xi'an",
            },
        }
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
