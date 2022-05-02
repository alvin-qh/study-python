import time
import timeit
from datetime import date, datetime

from dateutil import parser, tz

from .format import iso8601_format


class TestTime:
    """
    测试 `time` 包函数
    """

    def test_time_function(self) -> None:
        """
        `time` 函数用于获取一个浮点数表示的时间

        浮点数的整数部分表示自 1970 年之此时此刻的秒数, 小数部分表示到微秒的精度
        浮点数的精度是多少和系统的能力有关

        `time_ns` 函数可以将精度到纳秒
        """
        # 获取当前的秒数
        before = time.time()
        # 休眠 0.2 秒 (200 毫秒)
        time.sleep(0.2)
        # 获取休眠后的秒数
        after = time.time()
        # 两个时间相差的值在 200~300毫秒之间
        assert 0.2 <= after - before <= 0.21

    def test_other_time_function(self) -> None:
        """
        早期的日期时间函数, 和 C 标准库函数类似. 应该使用 `datetime` 包进行日期时间处理

        - `mktime` 函数, 通过一个表示本地时间的 `struct_time` 结构或一个 9 元组获取一个浮点秒
            - 9 元组为: (年, 月, 日, 时, 分, 秒, 星期, 全年第几天, 夏令时), 其中后三项一般不填
            - `struct_time` 和 9 元组对应为: `tm_year`, `tm_mon`, `tm_mday`,
              `tm_hour`, `tm_min`, `tm_sec`, `tm_wday`, `tm_yday` 和 `tm_isdst`

        - `localtime` 函数将一个浮点秒转换为本地时间的 `struct_time` 对象
            - 如果不填参数, 则表示获取当前的本地时间

        - `gmtime` 函数将一个浮点秒转换为 UTC 时间的 `struct_time` 对象
            - 如果不填参数, 则表示获取当前的 UTC 时间

        - `strftime` 函数将一个 `struct_time` 对象根据模式转为指定的字符串
        - `strptime` 函数将一个时间字符串还原为 `struct_time` 结构体
        """
        # 通过 9 元组获取指定日期时间的浮点秒
        tm = time.mktime((2022, 4, 1, 12, 13, 14, 0, 0, 0))
        assert tm == 1648786394.0

        # 将一个浮点秒转化为时间日期对象
        tl = time.localtime(tm)
        assert tl.tm_year == 2022
        assert tl.tm_mon == 4
        assert tl.tm_mday == 1
        assert tl.tm_hour == 12
        assert tl.tm_min == 13
        assert tl.tm_sec == 14
        assert tl.tm_wday == 4  # 周五
        assert tl.tm_yday == 91  # 全年第 91 天
        assert tl.tm_isdst == 0  # 非夏令时
        assert tl.tm_zone == "CST"  # 中国标准时间

        # 将一个时间日期对象转化为字符串
        s = time.strftime("%Y-%m-%dT%H:%M:%S", tl)
        assert s == "2022-04-01T12:13:14"

        # 将一个浮点秒转化为 UTC 日期时间对象
        tu = time.gmtime(tm)
        assert tu.tm_year == 2022
        assert tu.tm_mon == 4
        assert tu.tm_mday == 1
        assert tu.tm_hour == 4  # 和本地时间差 8 小时
        assert tu.tm_min == 13
        assert tu.tm_sec == 14
        assert tu.tm_wday == 4  # 周五
        assert tu.tm_yday == 91  # 全年第 91 天
        assert tu.tm_isdst == 0  # 非夏令时
        assert tu.tm_zone == "GMT"  # 格林尼治标准时间

        s = time.strftime("%Y-%m-%dT%H:%M:%S", tu)
        assert s == "2022-04-01T04:13:14"

        tl = time.strptime("2022-04-01T04:13:14", "%Y-%m-%dT%H:%M:%S")
        assert tl.tm_year == 2022
        assert tl.tm_mon == 4
        assert tl.tm_mday == 1
        assert tl.tm_hour == 4
        assert tl.tm_min == 13
        assert tl.tm_sec == 14
        assert tl.tm_wday == 4  # 周五
        assert tl.tm_yday == 91  # 全年第 91 天
        assert tl.tm_isdst == -1  # 是否夏令时未知
        assert tl.tm_zone is None  # 时区未知


class TestDatetime:
    """
    测试 `datetime` 包下面的 `date`, `time` ,`datetime` 和 `timedelta` 类

    标准的日期时间处理类
    """

    def test_date(self) -> None:
        """
        测试日期类型
        """
        # 定义一个日期类型
        d = date(2022, 4, 1)

        # 获取日期的年月日
        assert d.year == 2022
        assert d.month == 4
        assert d.day == 1

        # 获取日期的星期
        assert d.weekday() == 4  # 以周日为一周第一天计算, 4 为周五
        assert d.isoweekday() == 5  # 以周一为一周第一天算, 5 为周五

        # 格式化日期为标准字符串
        assert d.isoformat() == "2022-04-01"

        # 从标准字符串中还原日期对象
        assert date.fromisoformat("2022-04-01") == d

        # 获取今天的日期
        today = date.today()
        # 日期可进行比较
        assert d < today

    def test_time(self) -> None:
        pass

    def test_datetime(self) -> None:
        """
        测试时间日期类型
        """
        zone = "Asia/Shanghai"

        dt = datetime(2022, 4, 1, 12, 13, 14, tzinfo=tz.gettz(zone))
        assert dt.year == 2022
        # ... 省略其它日期时间分量测试
        assert dt.second == 14

        # 所有 date 类型的函数可以使用, 省略
        # 所有 time 类型的函数可以使用, 省略

        # 输出为标准字符串
        assert dt.isoformat() == "2022-04-01T12:13:14+08:00"
        # 从标准字符串还原
        assert datetime.fromisoformat("2022-04-01T12:13:14+08:00") == dt

        # 将时区转为 UTC 时区
        dt = dt.astimezone(tz=tz.UTC)
        # 输出为标准字符串
        assert dt.isoformat() == "2022-04-01T04:13:14+00:00"
        # 输出以 Z 结尾的 ISO8601 格式字符串
        assert iso8601_format(dt) == "2022-04-01T04:13:14Z"
        # dateutil.parser 的 isoparse 支持带 Z 后缀的时间格式
        assert parser.isoparse("2022-04-01T04:13:14Z") == dt


class TestTimeCount:
    """
    测试计时器函数
    包括 `time` 包下的 `perf_counter`, `process_time` 函数以及 `timeit` 包下
    的 `default_timer`, `timeit` 以及 `repeat` 函数
    """

    def test_perf_counter_function(self) -> None:
        """
        `time` 包的 `perf_counter` 函数用于获取一个浮点数表示的系统计时器值

        计时器的值是一个浮点秒, 无实际的时间含义. 但可以通过两个计时器的值计算时间差

        `perf_counter_ns` 函数可以将精度到纳秒
        """
        # 获取当前的计时器值
        before = time.perf_counter()
        # 休眠 0.2 秒 (200 毫秒)
        time.sleep(0.2)
        # 获取休眠后的计时器值
        after = time.perf_counter()
        # 两个时间相差的值在 200~300毫秒之间
        assert 0.2 <= after - before <= 0.31

    def test_process_time_function(self) -> None:
        """
        `time` 包的 `process_time` 函数用于获取进程对 CPU 占用的时间

        计时器的值是一个浮点秒, 无实际的时间含义. 但可以通过两个计时器的值计算时间差
        注意, 一旦当前进程不使用 CPU (例如线程被休眠或等待 IO), 这个计时器也不会增加

        `process_time` 函数可以将精度到纳秒
        """
        # 获取当前的计时器值
        before = time.process_time()
        # 休眠 0.2 秒 (200 毫秒)
        time.sleep(0.2)
        # 获取休眠后的计时器值
        after = time.process_time()
        # sleep 的时间不计算在内, 所以两个计数器的差值 ≈ 0
        assert 0 <= after - before <= 0.01

    def test_default_timer_function(self) -> None:
        """
        `timeit` 包的 `default_timer` 函数以最优方式返回计时器值

        在 Python2 中, 根据不同平台, 不同计时器的精度不同
        - 在 Win32 系统中, time.clock 函数精度较高
        - 在 Posix 系统中, time.time 函数精度高

        在 Python3 中 `default_timer` 函数固定为 `time` 包的 `perf_counter` 函数,
        `clock` 函数被弃用
        """
        # 获取当前的计时器值
        before = timeit.default_timer()
        # 休眠 0.2 秒 (200 毫秒)
        time.sleep(0.2)
        # 获取休眠后的计时器值
        after = timeit.default_timer()
        # sleep 的时间不计算在内, 所以两个计数器的差值 ≈ 0
        assert 0.2 <= after - before <= 0.21

    def test_timeit_function(self) -> None:
        """
        测试 `timeit` 包的 `timeit` 函数
        - `stmt` 要执行的代码, 可以是字符串或者实际代码. 如果是字符串, 则要注意无法使用当前代码
        的上下文, 相当于在一个新的沙盒内执行代码
        - `setup` 初始化的代码, 同 `stmt` 参数, 默认为 pass
        - `timer` 用于计时的函数, 默认为 `time.perf_counter` 函数
        - `number` 代码重复执行的次数, 默认为 `1`
        - `global` 一个 `Dict[str, Any]` 类型的字典, 会被设置为全局值, 默认为 `None`

        用于记录指定函数的执行性能
        """

        # 一段字符串表示的代码
        code = """
if num1 < num2:
    num1, num2 = num2, num1

while num2:
    num1, num2 = num2, num1 % num2"""

        # 测量以字符串形式表示的代码执行效率
        d = timeit.timeit(
            stmt=code,  # 要测量的代码
            setup="num1 = 1234\nnum2 = 5678",  # 初始化代码, 设置 num1 和 num2 变量的值
            number=int(1e6),
        )
        assert 0 < d < 1

        def calculate_gcd(num1: int, num2: int) -> int:
            """
            计算最大公约数

            Args:
                num1 (int): 第一个数
                num2 (int): 第二个数

            Returns:
                int: 两个数的最大公约数
            """
            if num1 < num2:
                num1, num2 = num2, num1

            while num2:
                num1, num2 = num2, num1 % num2

            return num1

        # 测量 Python 代码的执行效率
        d = timeit.timeit(
            stmt=lambda: calculate_gcd(1234, 5678),  # 测量 calculate_gcd 函数的执行效率
            number=int(1e6),
        )
        assert 0 < d < 1

    def test_repeat_function(self) -> None:
        """
        `timeit` 包下面的 `repeat` 函数用于重复执行一段代码若干次, 并返回每次执行的时长测量结果
        - `stmt` 要执行的代码, 可以是字符串或者实际代码. 如果是字符串, 则要注意无法使用当前代码
        的上下文, 相当于在一个新的沙盒内执行代码
        - `setup` 初始化的代码, 同 `stmt` 参数, 默认为 pass
        - `timer` 用于计时的函数, 默认为 `time.perf_counter` 函数
        - `repeat` 重复的次数, 默认为 `1`
        - `number` 代码重复执行的次数, 默认为 `1`
        - `global` 一个 `Dict[str, Any]` 类型的字典, 会被设置为全局值, 默认为 `None`

        """
        # 一段字符串表示的代码
        code = """
if num1 < num2:
    num1, num2 = num2, num1

while num2:
    num1, num2 = num2, num1 % num2"""

        # 重复 3 次, 测量字符串表示的代码
        ds = timeit.repeat(
            stmt=code,  # 要测量的代码
            setup="num1 = 1234\nnum2 = 5678",  # 初始化代码, 设置 num1 和 num2 变量的值
            repeat=3,  # 重复次数
        )
        assert len(ds) == 3

        def calculate_gcd(num1: int, num2: int) -> int:
            """
            计算最大公约数

            Args:
                num1 (int): 第一个数
                num2 (int): 第二个数

            Returns:
                int: 两个数的最大公约数
            """
            if num1 < num2:
                num1, num2 = num2, num1

            while num2:
                num1, num2 = num2, num1 % num2

            return num1

        # 重复 3 次, 测量 Python 代码的执行效率
        ds = timeit.repeat(
            stmt=lambda: calculate_gcd(1234, 5678),  # 测量 calculate_gcd 函数的执行效率
            repeat=3,
        )
        assert len(ds) == 3
