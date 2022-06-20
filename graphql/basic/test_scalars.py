from datetime import date, datetime, time

from .scalars import schema


def test_simple_scalar_types() -> None:
    """
    测试基本 Scalar 类型, 包括:
    - `ID`
    - `String`
    - `Int`
    - `Float`
    - `Boolean`
    """
    # 查询字符串
    query = """
        query getStuff {
            stuff {         #  对应 Query 类型的 stuff 字段
                id          #  对应 Stuff 类型的 id 字段
                name        #  对应 Stuff 类型的 name 字段
                serialNo    #  对应 Stuff 类型的 serial_no 字段
                price       #  对应 Stuff 类型的 price 字段
                lts         #  对应 Stuff 类型的 lts 字段
            }
        }
    """

    # 执行查询
    r = schema.execute(query)
    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "stuff": {
            "id": "1",
            "lts": True,
            "name": "Music Speaker",
            "price": 269.9,
            "serialNo": 101,
        },
    }


def test_datetime_scalar_types() -> None:
    """
    测试日期时间相关的 Scalar 类型, 包括:
    - `Date`
    - `DateTime`
    - `Time`
    """
    # 查询需 date, datetime, time 三个参数, 定义 $date, $datetime, $time 三个入参与之对应
    query = """
        query getCalendar($date: Date!, $datetime: DateTime!, $time: Time!) {
            calendar {                              # 对应 Query 类型的 calendar 字段
                oneWeekFrom(date: $date)            # 对应 Calendar 类型的 one_week_from 字段
                oneHourFrom(datetime: $datetime)    # 对应 Calendar 类型的 one_hour_from 字段
                oneMinuteFrom(time: $time)          # 对应 Calendar 类型的 one_minute_from 字段
            }
        }
    """

    # 设定入参的值
    now = datetime(2022, 6, 20, 12, 20, 0, 0)
    today = now.date()
    current = now.time()

    # 设定入参字典
    vars = {
        "date": today,  # 对应 $date 参数
        "datetime": now,  # 对应 $datetime 参数
        "time": current,  # 对应 $time 参数
    }

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询无错误
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "calendar": {
            "oneWeekFrom": "2022-06-27",  # 比入参多一周
            "oneHourFrom": "2022-06-20T13:20:00",  # 比入参多一小时
            "oneMinuteFrom": "12:21:00",  # 比入参多一分钟
        }
    }
