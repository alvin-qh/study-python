from datetime import datetime
from decimal import Decimal

from basic.scalars import schema


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
        query {
            stuff {         #  查询 Query 类型的 stuff 字段
                id          #  查询 Stuff 类型的 id 字段
                name        #  查询 Stuff 类型的 name 字段
                serialNo    #  查询 Stuff 类型的 serial_no 字段
                price       #  查询 Stuff 类型的 price 字段
                lts         #  查询 Stuff 类型的 lts 字段
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
        query ($date: Date!, $datetime: DateTime!, $time: Time!) {  # 设定查询参数
            calendar {                              # 查询 Query 类型的 calendar 字段
                oneWeekFrom(date: $date)            # 查询 Calendar 类型的 one_week_from 字段
                oneHourFrom(datetime: $datetime)    # 查询 Calendar 类型的 one_hour_from 字段
                oneMinuteFrom(time: $time)          # 查询 Calendar 类型的 one_minute_from 字段
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


def test_decimal_scalar_type() -> None:
    """
    测试 `Decimal` 类型
    """
    # 查询字符串
    query = """
        query ($number: Decimal!) {
            calculator {
                addOneTo(number: $number)
            }
        }
    """

    # 传入参数
    vars = {
        # 注意, 这里的 Decimal 类型是 Python 内置类型, 不是 Scalar 类型
        "number": Decimal(100.2),
    }

    # 执行查询
    result = schema.execute(query, variables=vars)
    # 确保查询正确
    assert result.errors is None

    # 确保结果正确
    assert result.data is not None
    val = Decimal(result.data["calculator"]["addOneTo"])
    assert val.quantize(Decimal("0.00")) == Decimal("101.20")


def test_json_string_scalar_type() -> None:
    """
    测试 `JSONString` 类型
    """
    # 查询字符串
    query = """
        query ($key: String!, $value: GenericType!) {   # 设定查询参数
        jsonObject {                                    # 查询 Query 类型的 json_object 字段
                updateJsonKey(key: $key, value: $value) # 查询 JSONObject 类型的 update_json_key 字段
            }
        }
    """

    # 传入参数
    vars = {
        "key": "name",  # 要修改的 json key 值
        "value": "Emma",  # 要修改的 json value 值
    }

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询正确
    assert r.errors is None

    # 确保结果正确, 服务端返回的 Dict 类型在这里表示为一个 json 字符串
    assert r.data == {"jsonObject": {"updateJsonKey": '{"name": "Emma", "age": 42}'}}


def test_custom_scalar_type() -> None:
    """
    测试 `Base64` 自定义 Scalar 类型
    """
    # 定义查询结构
    query = """
        query ($value: Base64!) {                   # 定义查询参数, 为自定义 Base64 类型
            encodedId {                             # 查询 Query 类型的 encoded_id 字段
                incrementEncodedId(value: $value)   # 查询 EncodedId 类型的 increment_encoded_id 字段
            }
        }
    """

    # 传入参数
    vars = {
        "value": "NA==",  # 参数为 "4" 的 base64 编码
    }

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果正确
    assert r.data == {
        "encodedId": {
            "incrementEncodedId": "NQ==",  # 返回结果为 "5" 的 base64 编码
        }
    }
