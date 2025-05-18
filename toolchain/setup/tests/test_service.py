from toolchain_setup.service.user_service import load_users


def test_load_user() -> None:
    users = load_users()
    assert len(users) == 2

    assert users[0].id == "U-001"
    assert users[0].name == "Alvin"
    assert users[0].password == "1234567"

    assert users[1].id == "U-002"
    assert users[1].name == "Emma"
    assert users[1].password == "7654321"
