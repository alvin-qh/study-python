import sched
import time
import timeit
from typing import Dict

from pytest import fail


def test_run_schedule_blocked() -> None:
    """计划任务

    - `sched` 包的 `scheduler` 函数用于创建一个计划任务对象
        - `time_func` 指定用于计算时间的函数, 该函数应返回秒数
        - `delay_func` 指定用于等待的函数
        - 返回一个 `scheduler` 对象

    - `scheduler` 对象的 `enter` 方法制定一个计划
        - `delay` 调用任务延迟秒数
        - `priority` 优先级, 当多个计划任务时间冲突时, 优先执行优先级高的计划
        - `action` 计划执行时调用的函数, 即计划任务
        - `argument` 传递给 action 函数的参数元组 (按参数顺序)
        - `kwargs` 传递给 action 函数的参数字典 (按参数名称)
        - 返回一个 `event` 对象, 表示该计划任务的存根

    - `schedule` 对象的 `run` 方法用于启动所有已制定的计划
        - `blocking` 参数为 `True`, 该函数会被阻塞, 直到所有计划任务执行完毕
    """

    # 产生一个计划对象
    schedule = sched.scheduler(
        timefunc=timeit.default_timer,  # 用于计时函数
        delayfunc=time.sleep,  # 用于等待的函数
    )

    # 记录开始时间
    start = timeit.default_timer()

    # 记录计划执行结果
    run_records: Dict[int, int] = {}

    def perform_command(id_: int) -> None:
        """计划执行函数, 当 schedule 计划到达时执行一次

        Args:
            - `id_` (`int`): 计划 id
        """
        run_records[id_] = int(timeit.default_timer() - start)

    # 制定 id=1 的计划，2秒后执行
    schedule.enter(2, 0, perform_command, argument=(1,))

    # 制定 id=2 的计划，1秒后执行
    schedule.enter(1, 0, perform_command, kwargs=dict(id_=2))
    schedule.run()

    # 计划执行完毕, 查看结果
    assert run_records == {
        2: 1,  # id=2 的计划在 1 秒后执行
        1: 2,  # id=1 的计划在 2 秒后执行
    }


def test_cancel_schedule() -> None:
    """撤销计划任务

    `schedule` 类的 `cancel(event)` 函数用于撤销一个计划. 注意, 只有尚未履行的计划任务可以撤销
    """

    def perform_command() -> None:
        """该任务会被取消, 所以不应当运行"""

        fail()

    # 实例化第一个计划对象
    schedule1 = sched.scheduler()

    # 2 秒后执行 perform_command 函数 (但实际会被取消, 不会执行)
    event = schedule1.enter(2, 0, perform_command)

    def cancel_schedule_event(event_: sched.Event) -> None:
        """用来取消已有任务的任务

        Args:
            - `event_` (`sched.Event`): 需要被取消的任务
        """
        schedule1.cancel(event_)

    # 实例化第二个计划对象
    schedule2 = sched.scheduler()

    # 1 秒后执行 cancel_schedule_event 函数, 取消前一个任务
    schedule2.enter(1, 0, cancel_schedule_event, kwargs={"event_": event})

    # 执行第二个计划对象
    while True:
        # 非阻塞执行, 返回下一个对象执行的时间
        next_ev = schedule2.run(blocking=False)

        # 返回 None 表示任务列表中已经无可执行任务
        if not next_ev:
            break

        # 休眠一段时间, 等待任务执行完毕
        time.sleep(next_ev)

    # 执行第一个计划对象, 但由于其中的任务已被取消, 所以无可执行任务
    schedule1.run()
