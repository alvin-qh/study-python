from peewee_.utils import run_once


def test_run_once() -> None:
    run_times = 0

    @run_once
    def run_once_func() -> int:
        nonlocal run_times
        run_times += 1

        assert run_times == 1
        return run_times

    assert run_once_func() == 1
    assert run_once_func() == 1
