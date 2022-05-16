import calendar
import time
import timeit
from datetime import date, datetime
from datetime import time as time_
from datetime import timedelta

from dateutil import parser
from dateutil import relativedelta as rd
from dateutil import tz

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
        assert tu.tm_zone in ("UTC", "GMT")  # 格林尼治标准时间

        # 格式化时间
        s = time.strftime("%Y-%m-%dT%H:%M:%S", tu)
        assert s == "2022-04-01T04:13:14"

        # 从字符串还原时间
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

        `datetime` 包下的 `date` 类型表示一个日期
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
        """
        测试时间类型

        `datetime` 包下的 `time` 类型表示一个时间
        """
        # 定义一个
        t = time_(12, 0, 0)
        assert t.hour == 12
        assert t.minute == 0
        assert t.second == 0
        assert t.microsecond == 0

        assert t.isoformat() == "12:00:00"

        t = time_(12, 0, 0, tzinfo=tz.UTC)
        assert t.tzname() == "UTC"
        assert t.utcoffset() == timedelta(hours=0)
        assert t.isoformat() == "12:00:00+00:00"

    def test_datetime(self) -> None:
        """
        测试时间日期类型

        `datetime` 包下的 `datetime` 类型表示一个完整的日期时间
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

    def test_timedelta(self) -> None:
        """
        测试时间差

        `datetime` 包下的 `timedelta` 类型表示两个时间的差值
        """
        t1 = datetime(2022, 4, 1, 12)
        t2 = datetime(2022, 4, 1, 16)

        # 计算两个时间的差值
        d = t2 - t1
        assert d == timedelta(hours=4)

        # 计算两个时间的差值
        d = t1 - t2
        assert d == timedelta(hours=-4)

        # 计算时间和一个时间差值的计算结果
        d = timedelta(hours=4)
        assert t2 == t1 + d
        assert t1 == t2 - d

        # 计算指定日期的前一个周日的日期
        t = t1 - timedelta(days=(t1.weekday() - calendar.SUNDAY) % 7)
        assert t == datetime(2022, 3, 27, 12)
        assert t.weekday() == calendar.SUNDAY

    def test_relativedelta(self) -> None:
        """
        更复杂的时间差类型

        `dateutil.relativedelta` 包下的 `relativedelta` 类型提供了更为复杂的时间差计算方式
        不仅可以计算两个时间的时间差, 也支持通过周, 天数, 闰年天等多个维度设置时间差
        """
        t1 = datetime(2022, 4, 1, 12)
        t2 = datetime(2022, 4, 1, 16)

        # 计算两个时间的时间差
        d = rd.relativedelta(t2, t1)
        assert d == rd.relativedelta(hours=4)

        # 设置时间差为 1 周
        d = rd.relativedelta(weeks=1)
        # 计算时间和时间差的计算结果
        assert t1 + d == datetime(2022, 4, 8, 12)

        t1 = datetime(2024, 3, 1, 12)
        # 设置时间差为 -1 闰年天
        # 当时间的年份是闰年, 且日期在 2月28日 之后, 这个时间差可以起作用
        d = rd.relativedelta(leapdays=-1)
        assert t1 + d == datetime(2024, 2, 29, 12)

    def test_datetime_parse(self) -> None:
        """
        测试 `datetime` 类型的字符串解析和格式化

        `datetime::strptime` 通过一个时间字符串和格式字符串还原一个日期时间对象
        日期时间对象的 `strftime` 通过一个格式字符串输出格式化结果
        """
        zone = "Asia/Shanghai"

        # 日期时间字符串
        s = "2022-04-01T12:13:14+0800"
        # 日期时间格式
        p = "%Y-%m-%dT%H:%M:%S%z"

        # 通过格式字符串将日期时间字符串进行解析
        # 得到一个日期时间对象
        d = datetime.strptime(s, p)
        assert d == datetime(2022, 4, 1, 12, 13, 14, tzinfo=tz.gettz(zone))

        # 日期时间对象通过格式字符串输出格式化结果
        assert d.strftime(p) == s

    def test_dateutil_parser(self) -> None:
        """
        `dateutil` 包下的 `parser` 对象可以对日期时间字符串做多种标准的解析
        """
        zone = "Asia/Shanghai"

        # 解析标准日期时间字符串
        d = parser.parse("2022-4-1 20:22:22")
        assert d == datetime(2022, 4, 1, 20, 22, 22)

        # 解析 ISO8601 格式日期时间字符串
        # 时区为 UTC 时区
        d = parser.parse("2022-4-1T20:22:22Z")
        assert d == datetime(2022, 4, 1, 20, 22, 22, tzinfo=tz.UTC)

        # 解析 ISO8601 格式日期时间字符串
        # 时区为东八区
        d = parser.parse("2022-4-1T20:22:22.1234+08:00")
        assert d == datetime(
            2022, 4, 1, 20, 22, 22, 123400, tzinfo=tz.gettz(zone),
        )

        # 解析 ISO8601 格式日期时间字符串
        # 忽略字符串中包含的时区信息
        d = parser.parse("2022-4-1T20:22:22.1234+08:00", ignoretz=True)
        assert d == datetime(2022, 4, 1, 20, 22, 22, 123400)

        # 解析一个带时区的时间字符串
        # 时区为东八区
        # default 参数表示一个默认的日期时间对象, 缺失的分量从这个对象中获取 (例如年月日)
        d = parser.parse("10:10+8:00", default=datetime(2022, 4, 1))
        assert d == datetime(
            2022, 4, 1, 10, 10, tzinfo=tz.gettz(zone),
        )

        # 解析斜杠分隔的日期
        # 月/日/年 格式
        d = parser.parse("4/1/22")
        assert d == datetime(2022, 4, 1)

        # 日/月/年 格式
        d = parser.parse("1/4/22", dayfirst=True)
        assert d == datetime(2022, 4, 1)

        # 年/月/日 格式
        d = parser.parse("22/4/1", yearfirst=True)
        assert d == datetime(2022, 4, 1)

        # 定义一个自定义时区字典
        #   自定义时区名称: 时区偏移量
        tzs = {
            "CN": tz.tzoffset(None, 8 * 3600),
            "US": tz.tzoffset(None, -4 * 3600),
        }

        # 解析自定义时区后缀的字符串
        d = parser.parse("2022-4-1 20:22:22 CN", tzinfos=tzs)
        assert d == datetime(2022, 4, 1, 20, 22, 22, tzinfo=tz.gettz(zone))

        # 解析自定义时区后缀的字符串
        d = parser.parse("2022-4-1 20:22:22 US", tzinfos=tzs)
        assert d == datetime(
            2022, 4, 1, 20, 22, 22, tzinfo=tz.gettz("America/New_York"),
        )

        # 模糊解析, 从字符串中摘取有效的日期时间信息
        s = "今天是 2022-4-1, 时间是 12:00:22, 时区为 +8:00"
        d = parser.parse(s, fuzzy=True)
        assert d == datetime(
            2022, 4, 1, 12, 0, 22, tzinfo=tz.gettz(zone),
        )


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
