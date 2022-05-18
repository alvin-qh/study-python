from datetime import datetime, timedelta

import pytz
from dateutil import tz


def test_locale_and_utc() -> None:
    """
    本地时间和 UTC 时间
    """
    # 获取本地时区的当前时间, 不包含时区信息
    t_loc = datetime.now()
    # 获取 UTC 时区的当前时间, 然后去除时区信息
    t_utc = datetime.now(tz=pytz.UTC).replace(tzinfo=None)

    # 两个时区时间相差 8 小时
    assert (t_loc - t_utc).total_seconds() // 3306 == 8.0


# 一个东八区时间
TIME = "2022-04-01T12:00:00+08:00"

# 无时区时间
TIME_WITHOUT_ZONE = "2022-04-01T12:00:00"

# 东八区时区名称
ZONE = "Asia/Shanghai"


def test_pytz() -> None:
    """
    测试 pytz 库的时区

    注意, pytz 的时区使用的时 LMT (Local Mean Time), 例如 Asia/Shanghai 这个时区并不是
    中国标准时区, 具体的值为 UTC+08:06, 即比标准中国时区多 6 分钟
    ! Asia/Shanghai 时区用于时区转换的结果是正确的, 但如果直接用其来设置时区则会出多 6 分钟的问题
    """
    # 获取内置的所有时区
    zones = pytz.all_timezones_set
    # 判断东八区是否存在
    assert ZONE in zones
    # 判断 UTC 是否存在
    assert "UTC" in zones

    # 产生一个无时区信息的时间
    t_nozone = datetime.fromisoformat(TIME_WITHOUT_ZONE)

    # 产生一个东八区时区
    tzinfo = pytz.timezone(ZONE)
    # 获取时区名称
    assert tzinfo.tzname(t_nozone) == "CST"
    # 获取时区偏移量
    assert tzinfo.utcoffset(t_nozone) == timedelta(hours=8)
    # 获取本地化时区时间 (不改变时间本身值, 只是赋予时区信息)
    assert tzinfo.localize(t_nozone).isoformat() == "2022-04-01T12:00:00+08:00"

    t = datetime(2022, 4, 1, 12, tzinfo=tzinfo)
    # 注意, Asia/Shanghai 这个时区比标准东八区多 6 分钟
    assert t.isoformat() == "2022-04-01T12:00:00+08:06"

    t = tzinfo.localize(datetime(2022, 4, 1, 12))
    # 用 pytz 时区的 localize 函数处理一个不带时区的时间, 可以得到正确的结果
    assert t.isoformat() == "2022-04-01T12:00:00+08:00"

    t = datetime(2022, 4, 1, 4, tzinfo=pytz.UTC)
    # 将 UTC 时间转为 Asia/Shanghai 时区结果是标准东八区
    t = t.astimezone(tzinfo)
    assert t.isoformat() == "2022-04-01T12:00:00+08:00"


def test_change_timezone() -> None:
    """
    通过 `datetime` 对象的 `astimezone` 方法可以改变当前时间的时区

    该操作会将时间改为符合所给时区的值
    """
    # 产生一个 东八区 时间
    t_loc = datetime.fromisoformat(TIME)
    # 确认时间部分
    assert t_loc.isoformat()[:19] == "2022-04-01T12:00:00"
    # 确认时间对象的时区名称
    assert t_loc.tzname() == "UTC+08:00"
    # 确认时区名称
    assert t_loc.tzinfo.tzname(t_loc) == "UTC+08:00"
    # 时区的时差为 8 小时
    assert t_loc.tzinfo.utcoffset(t_loc) == timedelta(hours=8)

    # 将东八区时间的时区改为 UTC
    t_utc = t_loc.astimezone(pytz.UTC)
    # UTC 时间和东八区相比差 8 小时
    assert t_utc.isoformat()[:19] == "2022-04-01T04:00:00"
    # 确认时间对象的时区名称
    assert t_utc.tzname() == "UTC"
    # 确认时区名称
    assert t_utc.tzinfo.tzname(t_utc) == "UTC"
    # 时区的时差为 0 小时
    assert t_utc.tzinfo.utcoffset(t_utc) == timedelta(hours=0)

    # 将 UTC 时间的时区改为东八区
    t_loc = t_utc.astimezone(pytz.timezone(ZONE))
    # 东八区时间和 UTC 时间相差 8 小时
    assert t_loc.isoformat()[:19] == "2022-04-01T12:00:00"
    # 确认时区名称, 因为本次时区是通过 Asia/Shanghai 字符串得到, 所以时区为 CST
    assert t_loc.tzname() == "CST"
    # 确认时区名称
    assert t_loc.tzinfo.tzname(t_loc) == "CST"
    # 时区的时差为 0 小时
    assert t_loc.tzinfo.utcoffset(t_loc) == timedelta(hours=8)


def test_replace_timezone() -> None:
    """
    强行替换时区

    `datetime` 对象的 `replace(tz=...)` 可以在不改变时间值的前提下, 更换一个新时区
    """
    # 产生一个 东八区 时间
    t_loc = datetime.fromisoformat(TIME)
    assert t_loc.isoformat()[:19] == "2022-04-01T12:00:00"
    assert t_loc.tzname() == "UTC+08:00"

    # 将东八区时间的时区强行换为 东八区 时区
    t_utc = t_loc.replace(tzinfo=pytz.UTC)
    assert t_utc.isoformat()[:19] == "2022-04-01T12:00:00"
    assert t_utc.tzname() == "UTC"

    # 将 UTC 时间的时区强行换为 UTC 时区
    t_loc = t_utc.replace(tzinfo=pytz.timezone(ZONE))
    assert t_loc.isoformat()[:19] == "2022-04-01T12:00:00"
    assert t_loc.tzname() == "LMT"


def test_create_timezone() -> None:
    """
    通过字符串定义时区信息

    POSIX1003.1 timezone string format:

        TZ  Timezone information. TZ has the form:

            stdoffset[dst[offset],[start[/time],end[/time]]]

        std and dst
            Three or more bytes that are the designation for the standard(std)
            and daylight savings time (dst) timezones. Only std is required.
            If dst is missing, then daylight savings time does not apply in
            this locale. Upper- and lower-case letters are allowed. Any
            characters except a leading colon (:), digits, a comma (,), a
            minus (-) or a plus (+) are allowed.

        offset
            Indicates the value one must add to the local time to arrive at
            Coordinated Universal Time.
            The offset has the form:

                hh[:mm[:ss]]

            The minutes (mm) and seconds (ss) are optional. The hour (hh) is
            required and may be a single digit. The offset following std is
            required. If no offset follows dst , daylight savings time is
            assumed to be one hour ahead of standard time. One or more digits
            may be used; the value is always interpreted as a decimal number.
            The hour must be between 0 and 24, and the minutes(and seconds)
            if present between 0 and 59. Out of range values may cause
            unpredictable behavior. If preceded by a "-" the timezone is east
            of the Prime Meridian; otherwise it is west(which may be indicated
            by an optional preceding "+" sign).

        start/time, end/time
            Indicate when to change to and back from daylight savings time,
            where start/time describes when the change from standard time to
            daylight savings time occurs, and end/time describes when the
            change back happens. Each time field describes when, in current
            local time, the change is made.

            The formats of start and end are one of the following:

            Jn      The Julian day n (1 < n < 365). Leap days are not counted.
                    That is, in all years, February 28 is day 59 and March 1
                    is day 60. It is impossible to refer to the occasional
                    February 29.

            n       The zero-based Julian day (0 < n < 365). Leap days are
                    counted, and it is possible to refer to February 29.

            Mm.n.d  The d**th day, (0 < d < 6) of week n of month m of the
            year (1 < n < 5, 1 < m < 12), where week 5 means "the last d-day
            in month m" which may occur in either the fourth or the fifth
            week). Week 1 is the first week in which the d**th day occurs.
            Day zero is Sunday.

            Implementation specific defaults are used for start and end if
            these optional fields are not given.

            The time has the same format as offset except that no leading
            sign ("-" or "+" is allowed. The default, if time is not given
            is 02:00:00.

        example: [continent/city] TZ=posix-tz-string
        1. without daylight saving example:
            [Pacific/Honolulu] TZ=HST10
            Where HST is the designation for the time zone (in this case
            Hawaii Standard Time) and 10 is the offset in hours. The offset
            indicates the value one must add to the local time to arrive at
            Coordinated Universal Time (UTC, aka GMT), and so it is positive
            for west of the meridian, e.g. America, and negative for east,
            e.g. China.

            [Asia/Beijing] TZ=CST-8
            Minutes and seconds are optional, so CST-8 and CST-08:00:00 mean
            the same thing. Note that the sign convention (+/-) used in a
            Posix TZ string is the opposite to that used in Internet time
            offsets (RFC 3339) and in Arthur David Olson's TZ data files.

        2. with daylight saving time example:
            [America/New_York] TZ=EST5EDT,M3.2.0/2,M11.1.0
            EST     = designation for standard time when daylight saving is
                      not in force
            5       = offset in hours = 5 hours west of Greenwich meridian
                      (i.e. behind UTC)
            EDT     = designation when daylight saving is in force (if omitted
                      there is no daylight saving)
            ,       = no offset number between code and comma, so default to
                      one hour ahead for daylight saving
            M3.2.0  = when daylight saving starts = the 0th day (Sunday) in the
                      second week of month 3 (March)
            /2,     = the local time when the switch occurs = 2 a.m. in this
                      case
            M11.1.0 = when daylight saving ends = the 0th day (Sunday) in the
                      first week of month 11 (November).
                      No time is given here so the switch occurs at 02:00 local
                      time.
                      So daylight saving starts on the second sunday in March
                      and finishes on the first Sunday in November. The switch
                      occurs at 02:00 local time in both cases. This is the
                      default switch time, so the /2 isn't strictly needed.

            [Europe/Paris] TZ=CET-1CEST,M3.5.0/2,M10.5.0/3
            CET     = designation for standard time when daylight saving is
                      not in force
            -1      = offset in hours = negative so 1 hour east of Greenwich
                      meridian
            CEST    = designation when daylight saving is in force ("Central
                      European Summer Time")
            ,       = no offset number between code and comma, so default to
                      one hour ahead for daylight saving
            M3.5.0  = when daylight saving starts = the last Sunday in March
                      (the "5th" week means the last in the month)
            /2,     = the local time when the switch occurs = 2 a.m. in this
                      case
            M10.5.0 = when daylight saving ends = the last Sunday in October.
            /3,     = the local time when the switch occurs = 3 a.m. in this
                      case
                      The European Union time zones are arranged so the switch
                      takes place at the same time in all zones.

            [America/St_Johns] TZ=NST03:30NDT,M3.2.0/0:01,M11.1.0/0:01
            Newfoundland's standard time is three and a half hours behind UTC
            with daylight saving begin on the second Sunday in March and
            ending on the first Sunday in November, but the switch occurs at
            one minute past midnight local time. As an extreme example,
            consider the mythical city of Foobar in Atlantis.

            [Atlantis/Foobar] TZ=AST2:45ADT0:45,M4.1.6/1:45,M10.5.6/2:45
            Atlantis Standard Time (AST) is 2 hours 45 minutes behind UTC and
            for daylight saving (ADT) they put their clocks forward two hours
            (i.e. to be 45 minutes behind UTC). Daylight saving starts on the
            first Saturday in April with the switch happening at 01:45 in the
            morning, and daylight saving ends on the last Saturday in October
            with the switch at 02:45 local time.
    """
    # 定义一个时区, 正常时间为 东 8 区 时间, 夏令时为 东 9 区 时间, 夏令时开始时间为 6 月
    # 第一个星期天到 9 月最后一个星期天
    # M6.1.0 即 6 月第一周第 0 天 (周日), M9.5.0 即 9 月 第 5 周 (最后一周) 第 0 天 (周日)
    tzinfo = tz.tzstr('RPC-8CRPC-9,M6.1.0/02:00,M9.5.0/10:00')

    # 测试正常时间区间
    t_rpc = datetime(2022, 4, 1, 20, 22, 22, tzinfo=tzinfo)
    assert t_rpc.isoformat() == "2022-04-01T20:22:22+08:00"

    # 测试夏令时时间区间
    t_crpc = datetime(2022, 7, 1, 10, 0, 0, tzinfo=tzinfo)
    assert t_crpc.isoformat() == "2022-07-01T10:00:00+09:00"
