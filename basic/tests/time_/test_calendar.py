import calendar as c
from datetime import date
from typing import List, Tuple, cast


class TestLeap:
    """测试日历的闰年功能"""

    def test_isleap(self) -> None:
        """`isleap` 函数用于判断一个年份是否闰年"""

        # 判断 2010 年是否闰年
        r = c.isleap(2010)
        assert not r

        # 判断 2000 年是否闰年
        r = c.isleap(2000)
        assert r

    def test_leapdays(self) -> None:
        """`leapdays` 函数用于获取两个年份间的有多少润天 (即多少闰年)"""

        # 获取 1900 年到 2000 年间的所有闰天
        r = c.leapdays(1900, 2000)
        assert r == 24


class TestWeekday:
    """测试日历的星期功能"""

    def test_weekday(self) -> None:
        """`weekday` 用于获取某个日期的星期"""

        # 获取 2015-10-01 日期的星期
        r = c.weekday(2015, 10, 1)
        assert r == c.THURSDAY  # 结果为星期四

    def test_monthrange(self) -> None:
        """`monthrange` 函数用于获取某个月份的第一天的星期和最后一天的日期"""

        # 获取 2015 年 10 月第一天的星期和最后一天日期
        r = c.monthrange(2015, 10)
        assert r == (c.THURSDAY, 31)  # 第一天为星期四, 最后一天为 31 号


class TestCalendarFunction:
    """测试日历相关的一组函数"""

    def test_setfirstweekday(self) -> None:
        """设置系统每周第一天是星期几"""

        # 将每周的第一天设置为周日
        c.setfirstweekday(c.SUNDAY)
        assert c.firstweekday() == c.SUNDAY

    @staticmethod
    def calendar_to_str(month_days: List[List[int]]) -> str:
        """月历数组转字符串

        将表示一个月日期的二维数组转为字符串

        Args:
            - `month_days` (`List[List[int]]`): 月历二维数组

        Returns:
            `str`: 月历字符串
        """
        # 星期字典
        weekdays = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}

        # 获取每周第一天是星期几
        start = c.firstweekday()

        # 生成第一行, 星期数
        cols = "  ".join([f"{weekdays[(start + n) % 7]}" for n in range(7)])
        # 生成日期
        cells = "\n  ".join(
            ["  ".join([f"{(day or ''):2}" for day in week]) for week in month_days]
        )
        return f"   {cols}\n  {cells}"

    def test_monthcalendar(self) -> None:
        """测试月历函数"""

        # 设置每周第一天为周日
        c.setfirstweekday(c.SUNDAY)

        # 获取月历数组
        mc = c.monthcalendar(2022, 4)
        assert mc == [
            [0, 0, 0, 0, 0, 1, 2],
            [3, 4, 5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14, 15, 16],
            [17, 18, 19, 20, 21, 22, 23],
            [24, 25, 26, 27, 28, 29, 30],
        ]

        # 月历数组转字符串
        assert (
            self.calendar_to_str(mc)
            == """   日  一  二  三  四  五  六
                       1   2
   3   4   5   6   7   8   9
  10  11  12  13  14  15  16
  17  18  19  20  21  22  23
  24  25  26  27  28  29  30"""
        )

        # 设置每周第一天为周一
        c.setfirstweekday(c.MONDAY)

        # 获取月历数组
        mc = c.monthcalendar(2022, 4)
        assert mc == [
            [0, 0, 0, 0, 1, 2, 3],
            [4, 5, 6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23, 24],
            [25, 26, 27, 28, 29, 30, 0],
        ]

        # 月历数组转字符串
        assert (
            self.calendar_to_str(mc)
            == """   一  二  三  四  五  六  日
                   1   2   3
   4   5   6   7   8   9  10
  11  12  13  14  15  16  17
  18  19  20  21  22  23  24
  25  26  27  28  29  30    """
        )

    def test_month(self) -> None:
        """测试输出月历字符串"""

        # 设置每周第一天为周一
        c.setfirstweekday(c.MONDAY)

        r = c.month(2022, 4)
        assert (
            r
            == """     April 2022
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30
"""
        )


class TestCalendarClass:
    """测试和日历相关的 `Calendar` 类型

    `Calendar` 类型可以独立对产生的对象进行配置, 避免因一些特殊场景污染全局配置
    """

    def test_iterweekdays(self) -> None:
        """根据设置每周的起始日期, 获取一周的星期排列"""

        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)
        # 获取一周排列
        r = ca.iterweekdays()
        # 以周日为第一天
        assert list(r) == [
            c.SUNDAY,
            c.MONDAY,
            c.TUESDAY,
            c.WEDNESDAY,
            c.THURSDAY,
            c.FRIDAY,
            c.SATURDAY,
        ]

        # 实例化日历对象, 设置每周的第一天为周四
        ca = c.Calendar(c.THURSDAY)
        # 获取一周排列
        r = ca.iterweekdays()
        # 以周四为第一天
        assert list(r) == [
            c.THURSDAY,
            c.FRIDAY,
            c.SATURDAY,
            c.SUNDAY,
            c.MONDAY,
            c.TUESDAY,
            c.WEDNESDAY,
        ]

    def test_itermonthdates(self) -> None:
        """`itermonthdates(year: int, month: int)` 方法用于获取一个 `datetime.date` 型月历

        返回结果的第一个元素为当月第一周第一天的日期. 如果当月 1 号不是第一周的第一天, 则使用上月日期补齐
        - `year` 年份
        - `month` 月份
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取当月月历 (第一天从周日开始), 转换为数组
        r = list(ca.itermonthdates(2022, 4))
        # 4 月 1 日是周五, 是月历开始的第 6 天
        # 所以结果长度为 35, 即包含了 35 个日期
        # 其中前 5 项为 3 月份的最后 5 天 (3-27 ~ 3-31)
        # 其中后 30 项为 4 月整月的 30 天 (4-1 ~ 4-30)
        assert len(r) == 35
        # 月历的第一天为周日, 是 3-27
        assert r[0] == date(2022, 3, 27)
        # 月历的最后一天为 4-30
        assert r[-1] == date(2022, 4, 30)

    def test_itermonthdays(self) -> None:
        """`itermonthdays(year: int, month: int)` 方法返回一个 `int` 型月历

        返回结果的第一个元素为当月第一周第一天的日期. 如果当月 1 号不是第一周的第一天, 则使用 0 补齐
        - `year` 年份
        - `month` 月份
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取当月月历 (第一天从周日开始), 转换为数组
        r = list(ca.itermonthdays(2022, 4))
        # 4 月 1 日是周五, 是月历开始的第 6 天
        # 所以结果长度为 35, 即包含了 35 个日期
        # 其中前 5 项为 0, 表示凑星期的补位
        # 其中后 30 项为 4 月整月的 30 天 (1 ~ 30)
        assert len(r) == 35
        # 月历的第一天为周日, 据 4-1 有 5 天差距, 所以月历的前 5 项为 0
        assert r[:5] == [0, 0, 0, 0, 0]
        # 月历从第 6 项开始为 1-30 的数字
        assert r[5:] == list(range(1, 31))

    def test_itermonthdays2(self) -> None:
        """`itermonthdays2(year: int, month: int)` 方法返回的月历包含 `(日, 星期)` 的信息

        如果当月 1 号不是一周第一天, 则返回结果的前若干项会用 `(0, 上月对应日期的星期)` 补齐
        - `year` 年份
        - `month` 月份
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取当月月历以及每天是周几, 从 4-1 号开始, 1 号之前的日期数为 0
        r = list(ca.itermonthdays2(2022, 4))
        # 4 月 1 日是周五, 是月历开始的第 6 天
        # 所以结果长度为 35, 即包含了 35 个日期
        # 其中前 5 项为 (0~5, 周日~周四), 表示凑星期的补位
        # 其中后 30 项为 4 月整月的 30 天 (1 ~ 30)
        assert len(r) == 35
        assert r[:5] == [
            (0, c.SUNDAY),
            (0, c.MONDAY),
            (0, c.TUESDAY),
            (0, c.WEDNESDAY),
            (0, c.THURSDAY),
        ]

        # 第 6 项为 4-1 日, 周五
        assert r[5] == (1, c.FRIDAY)
        # 最后一项为 4-30 日, 周六
        assert r[-1] == (30, c.SATURDAY)

    def test_monthdatescalendar(self) -> None:
        """`monthdatescalendar(year: int, month: int)` 方法返回二维数组, 包含当月的所有 周 以及每周的日期

        返回的数组包含整月所有周的数组, 周数组内包含完整一周的 `datetime.date` 元素
        - `year` 年份
        - `month` 月份
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取当月份周数组
        r = list(ca.monthdatescalendar(2022, 4))
        # 4 月份含 5 个周
        assert len(r) == 5

        # 第一周, 4 月只占第一周的后两天
        assert r[0] == [
            date(2022, 3, 27),  # 周日
            date(2022, 3, 28),  # 周一
            date(2022, 3, 29),  # 周二
            date(2022, 3, 30),  # 周三
            date(2022, 3, 31),  # 周四
            date(2022, 4, 1),  # 周五
            date(2022, 4, 2),  # 周六
        ]

        # 第二周
        assert r[1] == [
            date(2022, 4, 3),  # 周日
            date(2022, 4, 4),  # 周一
            date(2022, 4, 5),  # 周二
            date(2022, 4, 6),  # 周三
            date(2022, 4, 7),  # 周四
            date(2022, 4, 8),  # 周五
            date(2022, 4, 9),  # 周六
        ]

        # 第三周
        assert r[2] == [
            date(2022, 4, 10),  # 周日
            date(2022, 4, 11),  # 周一
            date(2022, 4, 12),  # 周二
            date(2022, 4, 13),  # 周三
            date(2022, 4, 14),  # 周四
            date(2022, 4, 15),  # 周五
            date(2022, 4, 16),  # 周六
        ]

        # 第四周
        assert r[3] == [
            date(2022, 4, 17),  # 周日
            date(2022, 4, 18),  # 周一
            date(2022, 4, 19),  # 周二
            date(2022, 4, 20),  # 周三
            date(2022, 4, 21),  # 周四
            date(2022, 4, 22),  # 周五
            date(2022, 4, 23),  # 周六
        ]

        # 第五周
        assert r[4] == [
            date(2022, 4, 24),  # 周日
            date(2022, 4, 25),  # 周一
            date(2022, 4, 26),  # 周二
            date(2022, 4, 27),  # 周三
            date(2022, 4, 28),  # 周四
            date(2022, 4, 29),  # 周五
            date(2022, 4, 30),  # 周六
        ]

    def test_monthdayscalendar(self) -> None:
        """`monthdayscalendar(year: int, month: int)` 方法返回二维数组包含当月的所有 周 以及每周的月天数

        返回的数组包含整月所有周的数组, 周数组内包含完整一周天数的 `int` 元素, 不在设定月份内的以 0 补齐
        - `year` 年份
        - `month` 月份
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取当月月历以及每天是周几, 从 4-1 号开始, 1 号之前的日期数为 0
        r = list(ca.monthdayscalendar(2022, 4))
        # 4 月份含 5 个周
        assert len(r) == 5

        # 第一周, 4 月只占第一周的后两天
        assert r[0] == [
            0,  # 周日
            0,  # 周一
            0,  # 周二
            0,  # 周三
            0,  # 周四
            1,  # 周五
            2,  # 周六
        ]

        # 第二周
        assert r[1] == [
            3,  # 周日
            4,  # 周一
            5,  # 周二
            6,  # 周三
            7,  # 周四
            8,  # 周五
            9,  # 周六
        ]

        # 第三周
        assert r[2] == [
            10,  # 周日
            11,  # 周一
            12,  # 周二
            13,  # 周三
            14,  # 周四
            15,  # 周五
            16,  # 周六
        ]

        # 第四周
        assert r[3] == [
            17,  # 周日
            18,  # 周一
            19,  # 周二
            20,  # 周三
            21,  # 周四
            22,  # 周五
            23,  # 周六
        ]

        # 第五周
        assert r[4] == [
            24,  # 周日
            25,  # 周一
            26,  # 周二
            27,  # 周三
            28,  # 周四
            29,  # 周五
            30,  # 周六
        ]

    def test_monthdays2calendar(self) -> None:
        """`monthdays2calendar(year: int, month: int)` 方法返回二维数组, 包含当月的所有 周 以及每周的月天数和星期

        返回的数组包含整月所有周的数组, 周数组内包含完整一周的 (月天数, 星期) 元素, 不在设定月份内的以 (0, 星期) 补齐
        - `year` 年份
        - `month` 月份
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取当月月历以及每天是周几, 从 4-1 号开始, 1 号之前的日期数为 0
        r = list(ca.monthdays2calendar(2022, 4))
        # 4 月份含 5 个周
        assert len(r) == 5

        # 第一周, 4 月只占第一周的后两天
        assert r[0] == [
            (0, c.SUNDAY),  # 周日
            (0, c.MONDAY),  # 周一
            (0, c.TUESDAY),  # 周二
            (0, c.WEDNESDAY),  # 周三
            (0, c.THURSDAY),  # 周四
            (1, c.FRIDAY),  # 周五
            (2, c.SATURDAY),  # 周六
        ]

        # 第二周
        assert r[1] == [
            (3, c.SUNDAY),  # 周日
            (4, c.MONDAY),  # 周一
            (5, c.TUESDAY),  # 周二
            (6, c.WEDNESDAY),  # 周三
            (7, c.THURSDAY),  # 周四
            (8, c.FRIDAY),  # 周五
            (9, c.SATURDAY),  # 周六
        ]

        # 第三周
        assert r[2] == [
            (10, c.SUNDAY),  # 周日
            (11, c.MONDAY),  # 周一
            (12, c.TUESDAY),  # 周二
            (13, c.WEDNESDAY),  # 周三
            (14, c.THURSDAY),  # 周四
            (15, c.FRIDAY),  # 周五
            (16, c.SATURDAY),  # 周六
        ]

        # 第四周
        assert r[3] == [
            (17, c.SUNDAY),  # 周日
            (18, c.MONDAY),  # 周一
            (19, c.TUESDAY),  # 周二
            (20, c.WEDNESDAY),  # 周三
            (21, c.THURSDAY),  # 周四
            (22, c.FRIDAY),  # 周五
            (23, c.SATURDAY),  # 周六
        ]

        # 第五周
        assert r[4] == [
            (24, c.SUNDAY),  # 周日
            (25, c.MONDAY),  # 周一
            (26, c.TUESDAY),  # 周二
            (27, c.WEDNESDAY),  # 周三
            (28, c.THURSDAY),  # 周四
            (29, c.FRIDAY),  # 周五
            (30, c.SATURDAY),  # 周六
        ]

    def test_yeardatescalendar(self) -> None:
        """`yeardatescalendar(year: int, width: int)` 方法返回一个 4 维数组, 包含一整年的日期

        第一维度是年数组, 包含了若干季度, 数量取决于 `width` 参数的设定. 第二维度是季度数组, 即 `width` 参数设定的每季度月份数.
        第三维度是月数组, 包含了一个月中所有的周. 第四维度是周数组, 包含了一周中的所有日期
        - `year` 年份
        - `width` 表示数组第一纬的宽度，可以理解为季度，默认为 `3`
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取年历, 按每 3 个月 (即一季度) 进行分隔
        r: List[List[List[List[date]]]] = cast(
            List[List[List[List[date]]]], ca.yeardatescalendar(2022, width=3)
        )

        # 全年四个季度
        assert len(r) == 4

        # 每季度三个月
        assert len(r[0]) == 3

        # 一月份 6 周
        assert len(r[0][0]) == 6

        # 一周 7 天
        assert len(r[0][0][0]) == 7

        # 一月份第一周日期
        assert r[0][0][0] == [
            date(2021, 12, 26),  # 周日
            date(2021, 12, 27),  # 周一
            date(2021, 12, 28),  # 周二
            date(2021, 12, 29),  # 周三
            date(2021, 12, 30),  # 周四
            date(2021, 12, 31),  # 周五
            date(2022, 1, 1),  # 周六
        ]

    def test_yeardayscalendar(self) -> None:
        """`yeardatescalendar(year: int, width: int)` 方法返回一个 4 维数组, 包含一整年的日期

        第一维度是年数组, 包含了若干季度, 数量取决于 `width` 参数的设定. 第二维度是季度数组, 即 `width` 参数设定的每季度月份数.
        第三维度是月数组, 包含了一个月中所有的周. 第四维度是周数组, 包含了一周中的所有的月天数, 超出当月的填充为 `0`
        - `year` 年份
        - `width` 表示数组第一纬的宽度，可以理解为季度，默认为 `3`
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取年历, 按每 3 个月 (即一季度) 进行分隔
        r: List[List[List[List[int]]]] = cast(
            List[List[List[List[int]]]], ca.yeardayscalendar(2022, width=3)
        )

        # 全年四个季度
        assert len(r) == 4

        # 每季度三个月
        assert len(r[0]) == 3

        # 一月份 6 周
        assert len(r[0][0]) == 6

        # 一周 7 天
        assert len(r[0][0][0]) == 7

        # 一月份第一周日期
        assert r[0][0][0] == [
            0,  # 周日
            0,  # 周一
            0,  # 周二
            0,  # 周三
            0,  # 周四
            0,  # 周五
            1,  # 周六
        ]

    def test_yeardays2calendar(self) -> None:
        """
        `yeardays2calendar(year: int, width: int)` 方法返回一个 4 维数组, 包含一整年的日期.
        第一维度是年数组, 包含了若干季度, 数量取决于 `width` 参数的设定. 第二维度是季度数组,
        即 `width` 参数设定的每季度月份数. 第三维度是月数组, 包含了一个月中所有的周. 第四维度是周
        数组, 包含了一周中的所有的 `(月天数, 星期数)`, 超出当月的 月天数 填充为 0
        - `year` 年份
        - `width` 表示数组第一纬的宽度，可以理解为季度，默认为 `3`
        """
        # 实例化日历对象, 设置每周的第一天为周日
        ca = c.Calendar(c.SUNDAY)

        # 获取年历, 按每 3 个月 (即一季度) 进行分隔
        r: List[List[List[List[Tuple[int, c.Day]]]]] = cast(
            List[List[List[List[Tuple[int, c.Day]]]]],
            ca.yeardays2calendar(2022, width=3),
        )

        # 全年四个季度
        assert len(r) == 4

        # 每季度三个月
        assert len(r[0]) == 3

        # 一月份 6 周
        assert len(r[0][0]) == 6

        # 一周 7 天
        assert len(r[0][0][0]) == 7

        # 一月份第一周日期
        assert r[0][0][0] == [
            (0, c.SUNDAY),  # 周日
            (0, c.MONDAY),  # 周一
            (0, c.TUESDAY),  # 周二
            (0, c.WEDNESDAY),  # 周三
            (0, c.THURSDAY),  # 周四
            (0, c.FRIDAY),  # 周五
            (1, c.SATURDAY),  # 周六
        ]


def test_to_unix_timestamp() -> None:
    """获取 Unix 时间戳, 即从 1970-01-01T00:00:00 开始的秒数"""

    # 获取 1970-01-01T00:00:00 的时间戳
    r = c.timegm((1970, 1, 1, 0, 0, 0))
    # 时间戳为 0, 是时间戳的零点时间
    assert r == 0

    # 获取 2022-04-01T00:00:00 的时间戳
    r = c.timegm((2022, 4, 1, 0, 0, 0))
    assert r == 1648771200
