from pytest import fixture


@fixture(scope="session", autouse=True)
def event_loop() -> None:
    import os

    os.environ["IS_TESTING"] = "True"
