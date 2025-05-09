from env import get_env


def test_get_value_from_env() -> None:
    val = get_env("USER_NAME")
    assert val == "Alvin"
