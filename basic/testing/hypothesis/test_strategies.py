import random
import re
from datetime import date, datetime, time, timedelta, tzinfo
from decimal import Decimal
from fractions import Fraction
from ipaddress import IPv4Address
from typing import (Any, Callable, Dict, FrozenSet, Iterable, List, Literal,
                    Set, Tuple, TypeVar, Union)
from xmlrpc.client import Boolean

import pytz
from hypothesis import assume, given, note
from hypothesis import strategies as st
from hypothesis.strategies._internal.core import RandomSeeder
from testing.hypothesis.strategies import User, UserStrategy


@given(bs=st.binary(min_size=10, max_size=20))
def test_strategies_binary(bs: bytes) -> None:
    """
    假设一组 `byte` 串并依次传递给测试参数, 函数定义如下:

    ```
    hypothesis.strategies.binary(
        *,
        min_size=0,     # 字节串最小允许长度
        max_size=None   # 字节串最大允许长度
    )
    ```

    本例中假设一组 10~20 之间的整数
    """
    # 判断生成的结果是一个 byte 串
    assert any(0x0 <= n <= 0xFF for n in bs)
    # 判断生成结果的长度符合预期
    assert 10 <= len(bs) <= 20


@given(b=st.booleans())
def test_strategies_booleans(b: Boolean) -> None:
    """
    假设一个 `Boolean` 类型值

    ```
    hypothesis.strategies.booleans()
    ```
    """
    assert isinstance(b, bool)


def format_num(num: int, unit: str) -> str:
    """
    格式化字符串, 合并数字和单位

    Args:
        num (int): 数字参数
        unit (str): 单位字符串

    Returns:
        str: 格式化后的字符串
    """
    return f"{num}{unit}"


@given(r=st.builds(
    format_num,  # 要调用的参数
    num=st.integers(),  # 为 format_num 函数假设的第一个参数
    unit=st.sampled_from(  # 为 format_num 函数假设的第二个参数
        ["mm", "cm", "m", "km"],
    ),
))
def test_strategies_builds(r: Any) -> None:
    """
    将指定函数的返回值依次传递给测试参数

    ```
    hypothesis.strategies.builds(
        target,     # 要调用的函数, 该函数的返回值会作为参数传递给测试函数
        /,
        *args,      # 要传递给 target 函数的参数, 按位置传递
        **kwargs    # 要传递给 target 函数的参数, 按参数名传递
    )
    ```

    本例中假设一组对 `format_num` 函数调用的结果
    """
    # 确认参数为字符串类型
    assert isinstance(r, str)

    # 确认参数是 数字 + 字母 组合
    m = re.match(r"[+-]?\d+(\w+)", r)
    assert m

    # 确认字母组合为所定义的单位字符串
    assert m.group(1) in {"mm", "cm", "m", "km"}


@given(c=st.characters(
    min_codepoint=ord("A"),  # 假设的字符从 A 字符开始
    max_codepoint=ord("Z"),  # 假设的字符到 Z 字符结束
    whitelist_characters="abc",  # 额外传递 a, b, c 三个字符
    blacklist_characters="XY",  # 过滤掉 X, Y 两个字符
    whitelist_categories=("Cs",),  # 允许 Cs 分类中的字符
    blacklist_categories=("Cc", )  # 过滤掉 Cc 分类中的字符
))
def test_strategies_characters(c: str) -> None:
    """
    假设一组字符并依次传递给测试参数

    ```
    hypothesis.strategies.characters(
        *,
        min_codepoint=None,         # 假设字符的最小 unicode 编码
        max_codepoint=None,         # 假设字符的最大 unicode 编码
        whitelist_characters=None,  # 字符白名单, 其内的字符一定会传递给测试参数
        blacklist_characters=None,  # 字符黑名单, 其内的字符会被过滤掉, 不传递给测试参数
        whitelist_categories=None,  # unicode 类别白名单, 在此类别中的字符会传递给测试参数
        blacklist_categories=None   # unicode 类别黑名单, 在此类别中的字符不会传递给测试参数
    )
    ```

    备注: 所谓 Unicode 类别, 即对 Unicode 字符的一个分类, 具体参考:
    https://unicodeplus.com/category
    https://wikipedia.org/wiki/Unicode_character_property

    本例中假设一组 A~Z 的字符
    """
    assert len(c) == 1

    if ord("A") <= ord(c) <= ord("Z"):
        assert c not in {"X", "Y"}
    else:
        assert c in {"a", "b", "c"}


@given(c=st.complex_numbers(
    min_magnitude=1.0,  # 假设值所允许的最小值
    max_magnitude=100.0,  # 假设值所允许的最大值
))
def test_strategies_complex_numbers(c: complex) -> None:
    """
    假设一组复数并依次传递给测试参数

    ```
    hypothesis.strategies.complex_numbers(
        *,
        min_magnitude=0,     # 假设值所允许的最小值
        max_magnitude=None,  # 假设值所允许的最大值
        allow_nan=None,      # 是否允许假设 NaN 数值
        allow_infinity=None, # 是否允许假设 INF 数值
        allow_subnormal=True # 是否允许非规格化浮点数
                          # 参考: https://en.wikipedia.org/wiki/Subnormal_number
    )
    ```

    本例中假设了一组 1.0~100.0 的复数
    """
    # 复数不为 0, 即 0
    assert c

    # 确认复数 c 在指定的范围
    # abs(c) 有可能会存在浮点数精度问题, 所以比较的时候范围需要略微放宽
    assert 0 <= abs(c) < 101


E = TypeVar("E")


@st.composite
def element_and_index(
    draw: st.DrawFn,
    element: st.SearchStrategy[E],
) -> Tuple[int, E]:
    """
    利用 `@composite` 装饰器产生一个假设组合, 其定义如下:

    ```
    # 装饰器修饰的函数, f 参数类型为 Callable[[DrawFn, SearchStrategy], Any]
    hypothesis.strategies.composite(f)
    ```

    Args:
        draw (st.DrawFn): 产生指定假设的函数
        element (st.SearchStrategy[E]): 产生假设的 `Strategy` 类

    Returns:
        Tuple[int, E]: 输出的假设值
    """
    # 根据传入的假设类型产生假设值
    elem = draw(element)

    # 产生一个整数假设值
    index = draw(st.integers(min_value=1, max_value=1000))

    # 返回假设值组合
    return (index, elem)


@given(r=element_and_index(  # 产生一组假设, 一部分为通过 text 函数产生的假设值
    st.text(  # 假设一组字符串类型的参数
        min_size=1,
        alphabet=st.characters(
            min_codepoint=ord("A"),
            max_codepoint=ord("z"),
        ),
    ),
))
def test_composite(r: Tuple[int, str]) -> None:
    """
    组合多种假设方法, 统一产生一个结果

    参考 `element_and_index` 函数实现
    """
    note(f"argument r={r}")

    # 确保 r 参数类型为二元组
    assert len(r) == 2

    # 确保二元组的每个元素类型
    assert isinstance(r[0], int)
    assert isinstance(r[1], str)

    # 确保二元组的取值范围
    assert 1 <= r[0] <= 1000


@given(d=st.data())
def test_strategies_data(d: st.DataObject) -> None:
    """
    提供 `draw` 方法, 通过一组 `SearchStrategy` 类型对象产生所需假设值, 其定义如下:

    ```
    hypothesis.strategies.data()
    ```
    """
    # 通过 draw 方法产生两个假设值
    n1 = d.draw(st.integers())
    n2 = d.draw(st.integers(min_value=n1))

    # 排除掉 n1 == n2 的情况
    assume(n1 != n2)

    # 执行断言
    assert n1 < n2


start_datetime = datetime(2000, 1, 1, 0, 0, 0)
end_datetime = datetime(2030, 12, 31, 23, 59, 59)


@given(d=st.dates(
    min_value=start_datetime.date(),  # 假设日期的最小值
    max_value=end_datetime.date(),  # 假设日期的最大值
))
def test_strategies_dates(d: date) -> None:
    """
    假设一组日期, 并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.dates(
        min_value=datetime.date.min,  # 假设日期所允许的最小值
        max_value=datetime.date.max   # 假设日期所允许的最大值
    )
    ```

    假设一组 `start_datetime.date()` 和 `end_datetime.date()` 之间的日期
    """
    assert isinstance(d, date)
    assert start_datetime.date() <= d <= end_datetime.date()


@given(d=st.datetimes(
    min_value=start_datetime,
    max_value=end_datetime,
    timezones=st.timezones(),
))
def test_strategies_datetimes(d: datetime) -> None:
    """
    假设一组时间日期对象, 并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.datetimes(
        min_value=datetime.datetime.min, # 假设日期时间所允许的最小值
        max_value=datetime.datetime.max, # 假设日期时间所允许的最大值
        *,
        timezones=none(),       # 假设日期时间所属的时区
        allow_imaginary=True    # 是否过滤掉 "假象" 时间 (夏令时, 闰秒, 时区等)
    )
    ```

    假设一组 `start_datetime` 和 `end_datetime` 之间的日期时间
    """
    assert isinstance(d, datetime)

    # 确保假设的时间日期带有时区信息
    assert d.tzinfo

    # 去除假设日期时间中的时区信息
    d = d.replace(tzinfo=None)

    # 确认假设的日期时间在指定的范围内
    assert start_datetime <= d <= end_datetime


@given(n=st.decimals(
    min_value=Decimal(0.0),  # 假设所允许的最小值
    max_value=Decimal("1e100"),  # 假设所允许的最大值
    places=3,  # 假设数值的小数位
))
def test_strategies_decimals(n: Decimal) -> None:
    """
    假设一组 `Decimal` 类型数值, 并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.decimals(
        min_value=None, # 假设值允许的最小值
        max_value=None, # 假设值允许的最大值
        *,
        allow_nan=None, # 是否允许产生 NaN 值 (非数字)
        allow_infinity=None, # 是否允许产生 INF 值 (无穷)
        places=None # 是否指定固定的小数位数
    )
    ```

    假设一组 0.0~1e100 之间的 `Decimal` 类型数值
    """
    # 确认假设值的类型
    assert isinstance(n, Decimal)

    # 确认假设值的范围
    assert Decimal(0.0) <= n <= Decimal("1e100")

    # 确认假设值的小数位数
    sn = str(n)
    assert len(sn) - 1 - sn.rindex(".") == 3


def test_strategies_deferred() -> None:
    """
    允许一个假设引用另一个尚未定义的假设, 通过之后定义的假设产生值

    注意: 这并不是意味着要把后一个假设的值用于前一个假设, 而是通过后一个假设定义为前一个假设
    产生值, 所以两个假设的值并不相同
    """
    # 假设 a 引用假设 b, 此时假设 b 尚未定义
    a = st.deferred(lambda: b)

    # 再假设 a 后定义假设 b
    b = st.integers()

    # 确定假设 a 通过假设 b 产生值
    assert isinstance(a.example(), int)


@given(d=st.dictionaries(
    keys=st.from_regex(r"[a-z]{3}", fullmatch=True),  # 假设任意三个字母作为 key
    values=st.integers(  # 假设任意 1~100 整数作为 value
        min_value=1,
        max_value=100,
    ),
))
def test_strategies_dictionaries(d: Dict) -> None:
    """
    假设一组字典对象, 并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.dictionaries(
        keys,       # 字典 key 的假设方法
        values,     # 字典 value 的假设方法
        *,
        dict_class=<class 'dict'>, # 字典类型
        min_size=0,     # 字典内最小键值对数量
        max_size=None   # 字典内最大键值对梳理
    )
    ```

    注意: 每次假设的字典对象, 其包含的键值对数量并不确定, 介于空字典到若干键值对之间

    本例中假设一组动态字典对象
    """
    # 过滤掉空字典对象, 也可以通过 min_size 设置非空字典
    assume(d)

    # 遍历所有的 key
    for k in d.keys():
        assert isinstance(k, str)  # 确认 key 为字符串类型
        assert len(k) == 3  # 确认 key 的长度为 3
        assert k.isalpha()  # 确认 key 全部为英文字母

    # 遍历所有的 value
    for v in d.values():
        assert isinstance(v, int)  # 确认 value 为整型
        assert 1 <= v <= 100  # 确认 value 值的假设范围


@given(e=st.emails())
def test_strategies_emails(e: str) -> None:
    """
    假设一组 email 地址, 并传入测试参数, 定义如下:

    ```
    hypothesis.strategies.emails()
    ```
    """
    # 判断假设的值是否匹配 email 格式
    assert re.match(r"^.*?@(.*?\.)*.+?$", e)


@given(d=st.fixed_dictionaries(  # type: ignore
    mapping={  # 设置必要的字典模板
        "name": st.from_regex(r"[a-z]{3,5}", fullmatch=True),
        "gender": st.from_regex(r"M|F", fullmatch=True),
    },
    optional={  # 设置可选的字典模板
        "age": st.integers(min_value=20, max_value=50),
    }
))
def test_strategies_fixed_dictionaries(d: Dict) -> None:
    """
    假设一个固定 key 的字典对象

    ```
    hypothesis.strategies.fixed_dictionaries(
        mapping,        # 字典模板, 即字典 key 对应 value 产生的规则
        *,
        optional=None   # 可选模板
    )
    ```

    本例中假设了一组固定 key 的字典对象
    """
    # 确保假设的字典对象包含两项
    assert len(d) in (2, 3)

    # 确保 name 字段包含 3~5 个字符
    assert 3 <= len(d["name"]) <= 5

    # 确保 name 字段全部由小写字符组成
    for c in d["name"]:
        assert ord("a") <= ord(c) <= ord("z")

    # 确保 gender 字段由 M 和 F 字符构成
    assert d["gender"] in ("M", "F")

    # 确保 age 字段的数值范围
    if len(d) == 3:
        assert 20 <= d["age"] <= 50


@given(n=st.floats(
    min_value=0.0,  # 假设值的最小允许值
    max_value=0.1,  # 假设值的最大允许值
))
def test_strategies_floats(n: float) -> None:
    """
    假设一个 `float` 类型的值, 并传递给测试参数, 定义如下：

    ```
    hypothesis.strategies.floats(
        min_value=None,  # 假设值的最小允许值
        max_value=None,  # 假设值得最大允许值
        *,
        allow_nan=None,  # 是否允许假设 NaN 值
        allow_infinity=None,  # 是否允许假设 INF 值
        allow_subnormal=None, # 是否允许非规格化浮点数
                           # 参考: https://en.wikipedia.org/wiki/Subnormal_number
        width=64,   # 浮点数的宽度, 默认为 64bit
        exclude_min=False,  # 如果为 True, 则不包含 min_value 值
        exclude_max=False   # 如果为 True, 则不包含 max_value 值
    )
    ```

    本例中假设了一组 0.0~0.1 之间的浮点数
    """
    # 确认参数的类型
    assert isinstance(n, float)

    # 确认参数的范围
    assert 0.0 <= n <= 0.1


@given(f=st.fractions(
    min_value=1/2,  # 假设值所允许的最小值
    max_value=1,  # 假设值所允许的最大值
    max_denominator=10,  # 假设值允许的最大分母值
))
def test_strategies_fractions(f: Fraction) -> None:
    """
    假设一组分数值, 并传递给测试参数, 定义如下:

    ```
    hypothesis.strategies.fractions(
        min_value=None,  # 假设值最小允许值
        max_value=None,  # 假设值最大允许值
        *,
        max_denominator=None  # 分母允许的最大值
    )
    ```

    本例中假设了一组 1/2~1 之间的分数, 分母最大值为 10
    """
    # 确认参数类型
    assert isinstance(f, Fraction)

    # 确认假设值的范围
    assert 1/2 <= float(f) <= 1

    # 确认假设值的最大分母值范围
    assert f.denominator <= 10


@given(s=st.from_regex(
    regex=r"(13[0-9]|14[579]|15[0-35-9]|16[6]|17[0135678]|18[0-9]|19[89])"
          r"[0-9]{8}",
    fullmatch=True,  # 是否全量匹配
))
def test_strategies_from_regex(s: str) -> None:
    """
    通过指定的正则表达式定义假设一组值, 传递给测试参数

    ```
    hypothesis.strategies.from_regex(
        regex,          # 正则表达式模板
        *,
        fullmatch=False # 是否需要完全匹配正则表达式模板
    )
    ```

    本例中假设了一组符合正则表达式的手机号码进行测试
    注意: `\\d` 会产生各类 Unicode 字符的数字 (例如罗马数字), 所以不能简单的用 `\\d`,
    而是 `[0-9]`, 限定为阿拉伯数字
    """
    assert len(s) == 11
    assert s[0] == "1"


@given(
    u=UserStrategy(
        st.from_regex(r"[A-Z][a-z]{3,5}", fullmatch=True)
    )
    .filter(lambda u: len(u.name) > 0)
)
def test_custom_strategy(u: User) -> None:
    """
    自定义假设类型

    自定义假设类型的对象可以产生自定义的数据类型

    本例中通过 `UserStrategy` 类型假设一组 `User` 类型对象并传入测试参数
    """
    # 确认参数为 User 类型
    assert isinstance(u, User)

    # 确认 name 属性的首字母为大写字母
    assert ord("A") <= ord(u.name[0]) <= ord("Z")

    # 确认 name 属性的长度范围
    assert 4 <= len(u.name) <= 6

    # 确认 name 属性的后续字符为小写字母
    assert all([ord("a") <= ord(c) <= ord("z") for c in u.name[1:]])


@given(n=st.from_type(thing=int))
def test_strategies_from_regular_type(n: int) -> None:
    """
    从给定的类型中假设一组值, 并传递给测试参数
    """
    # 确认参数类型和指定类型相同
    assert isinstance(n, int)


@given(u=st.from_type(thing=User))
def test_strategies_from_custom_type(u: User) -> None:
    """
    从给定的类型中假设一组值, 并传递给测试参数
    """
    # 确认参数类型符合指定的类型
    assert isinstance(u, User)

    # 确认 name 属性的首字母为大写字母
    assert ord("A") <= ord(u.name[0]) <= ord("Z")

    # 确认 name 属性的长度范围
    assert 4 <= len(u.name) <= 6

    # 确认 name 属性的后续字符为小写字母
    assert all([ord("a") <= ord(c) <= ord("z") for c in u.name[1:]])


@given(st.frozensets(
    elements=st.integers(),
    min_size=1,
    max_size=10,
))
def test_strategies_frozensets(fs: FrozenSet) -> None:
    """
    假设一个 `FrozenSet` 对象, 即一个不可修改的 Set 集合, 并传递给测试参数

    ```
    hypothesis.strategies.frozensets(
        elements,       # 集合元素值的假设定义
        *,
        min_size=0,     # 集合的最小长度
        max_size=None   # 集合的最大长度
    )
    ```

    本例假设了一个长度在 `1`~`10` 之间的 `FrozenSet` 集合, 元素类型为 `int` 类型
    """
    # 确保参数类型为 `FrozenSet`
    assert isinstance(fs, FrozenSet)

    # 确认集合长度的范围
    assert 1 <= len(fs) <= 10

    # 确认集合元素类型
    for n in fs:
        assert isinstance(n, int)


@given(st.functions(
    like=lambda n: ...,  # 设置参数为整数类型的函数定义
    returns=st.from_regex(r"[0-9]{3,5}", fullmatch=True),  # 设置假设函数的返回值假设
))
def test_strategies_functions(fn: Callable[[int], str]) -> None:
    """
    假设一个函数, 并指定函数的定义和返回值的假设规则, 其定义如下:

    ```
    hypothesis.strategies.functions(
        *,
        like=lambda: ...,  # 设置假设函数的定义
        returns=...,       # 设置假设函数的返回值, 是一个假设规则
        pure=False         # 是否为纯函数, 若为纯函数, 则入参必须可哈希, 且入参相同返回
                           # 的结果也相同
    )
    ```
    """
    # 调用假设的函数
    r = fn(100)

    # 确保假设函数返回字符串类型返回值
    assert isinstance(r, str)

    # 确认返回结果
    assert re.match(r"[0-9]{3,5}", r)


@given(n=st.integers(
    min_value=1,  # 假设值的最小值
    max_value=100,  # 假设值的最大值
))
def test_strategies_integers(n: int) -> None:
    """
    假设一组整数, 并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.integers(
        min_value=None,  # 假设值的最小值
        max_value=None   # 假设值的最大值
    )
    ```

    本例中假设了一组 `1`~`100` 之间的整数
    """
    # 确保参数类型
    assert isinstance(n, int)

    # 确保假设值的取值范围
    assert 1 <= n <= 100


@given(ip=st.ip_addresses(
    v=4,  # 使用 IPv4 协议
    network="192.168.1.0/24"  # 设置子网掩码为一个 C 类 IP 子网掩码
))
def test_strategies_ip_addresses(ip: IPv4Address) -> None:
    """
    假设一个指定掩码的 IP 地址, 并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.ip_addresses(
        *,
        v=None,       # 指定 IP 地址的版本, 可以为 4 和 6
        network=None  # 指定子网掩码
    )
    ```

    子网掩码计算规则:
    1. CIDR 标准的 `/24` 表示的子网掩码为 `11111111 11111111 11111111 00000000`,
       即 `255.255.255.0`
    2. 该掩码下可用的主机地址为 `254` 个

    对于 `192.168.1.0/24`, C 类子网掩码, 可容纳 `254` 个主机,
    即 `192.168.1.0 ~ 192.168.1.254`
    """
    # 确保参数为字符串类型
    assert isinstance(ip, IPv4Address)

    # 确保假设的为指定的 IP 地址
    assert re.match(r"192\.168\.1\.\d?\d?\d", str(ip))


@given(it=st.iterables(
    elements=st.integers(min_value=1, max_value=20),  # 设置迭代器的元素假设规则
    min_size=1,  # 迭代器最小元素个数
    max_size=10,  # 迭代器最大元素个数
    unique_by=lambda n: n,  # 计算元素唯一性的依据
))
def test_strategies_iterables(it: Iterable[int]) -> None:
    """
    假设一组可迭代对象, 并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.iterables(
        elements,       # 迭代器元素的假设规则
        *,
        min_size=0,     # 迭代器元素的最小个数
        max_size=None,  # 迭代器元素的最大个数
        unique_by=None, # 返回用于计算集合唯一性值的函数
        unique=False    # 是否令元素唯一, 对于简单元素类型适用, 和 unique_by 参数二选一
    )
    ```

    本例中假设一组长度为 1~10 之间, 元素类型为 int 类型, 元素唯一的可迭代对象
    """
    # 确保参数为可迭代类型
    assert isinstance(it, Iterable)

    # 确保迭代器元素值的唯一性
    lst = list(it)
    assert len(set(lst)) == len(lst)


@given(v=st.just("Hello"))
def test_strategies_just(v: Any) -> None:
    """
    假设一个固定值并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.just(value)
    ```

    `just` 函数返回给定参数的一个拷贝, 用于在假设中产生特定值
    """
    # 确保参数类型为字符串类型, 和传递给 just 参数的参数类型一致
    assert isinstance(v, str)

    # 确认参数的值, 和传递给 just 参数的参数值一致
    assert v == "Hello"


@given(st.lists(
    elements=st.integers(min_value=1, max_value=10),  # 集合元素的假设规则
    min_size=10,  # 集合元素数量最小值
    max_size=10,  # 集合元素数量最大值
    unique_by=lambda n: n,  # 返回用于计算唯一性值得函数
))
def test_strategies_lists(lst: List[int]) -> None:
    """
    假设一组列表集合对象, 并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.lists(
        elements,       # 集合元素值得假设规则
        *,
        min_size=0,     # 集合最小元素个数
        max_size=None,  # 集合最大元素个数
        unique_by=None, # 返回用于计算集合唯一性值的函数
        unique=False    # 集合元素是否唯一, 对于简单元素类型适用, 和 unique_by 二选一
    )
    ```
    """
    # 确保参数为 List 类型
    assert isinstance(lst, List)

    # 确保结合元素值唯一性
    assert len(set(lst)) == len(lst)

    # 确保集合元素值类型为 int
    for n in lst:
        assert isinstance(n, int)


@given(v=st.one_of(  # 在指定的假设定义中人选其一
    st.integers(),
    st.none(),
    st.text(),
))
def test_strategies_one_of(v: Union[int, Literal[None], str]) -> None:
    """
    从给定的若干个假设定义中产生一个假设值并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.one_of(
        *args   # 若干个假设规则定义, 返回值即从这些假设规则中产生
    )
    ```
    """
    # 确保参数类型在指定的假设定义范围内
    if v is not None:
        assert isinstance(v, (int, str))


@given(st.permutations(
    values=[1, 2, 3, 4, 5]
))
def test_strategies_permutations(v: List[int]) -> None:
    """
    根据所给的列表, 假设一组元素相同, 但打乱顺序的列表并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.permutations(
        values  # 所给的列表, 再此基础上打乱顺序
    )
    ```
    """
    # 确认参数类型为列表集合
    assert isinstance(v, List)

    # 确认参数列表元素和原始列表元素相同
    assert set(v) == {1, 2, 3, 4, 5}


@given(r=st.random_module())
def test_strategies_random_module(r: RandomSeeder) -> None:
    """
    返回产生随机数的种子对象

    ```
    hypothesis.strategies.random_module()
    ```
    """
    assert isinstance(r.seed, int)


@given(r=st.randoms(
    note_method_calls=True,
    use_true_random=True,
))
def test_strategies_randoms(r: random.Random) -> None:
    """
    假设一个随机数生成器对象, 并传递给测试参数, 其定义如下：

    ```
    hypothesis.strategies.randoms(
        *,
        note_method_calls=False,
        use_true_random=False
    )
    ```
    """
    assert isinstance(r, random.Random)


@given(r=st.recursive(
    base=st.integers(min_value=1, max_value=10),  # 定义基础假设规则
    extend=lambda b: st.lists(b, min_size=2),  # 定义递归函数
    max_leaves=3,  # 定义最大递归次数
))
def test_strategies_recursive(r) -> None:
    """
    用递归方法进行假设, 并将结果传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.recursive(
        base,     # 基础假设规则
        extend,   # 递归函数
        *,
        max_leaves=100  # 最大的递归次数
    )
    ```

    递归执行的过程如下:
    1. 实例化 `base` 定义的假设对象;
    2. 调用 `extend` 定义的函数 `0` ~ `max_leaves` 次;
    3. 每次调用 `extend` 函数, 传入 `base` 假设的值或前一次 `extend` 函数的返回值

    例如:
    ```
    recursive(
        base=integers(),
        extend=lambda b: lists(b, min_size=2),
        max_leaves=3,
    )
    ```
    - 首先调用 `base`, 得到一个 `int` 类型假设对象;
    - 如果调用 `extend` 函数 `0` 次, 则最终返回结果为一个 `int` 值， 即 `n`;
    - 如果调用 `extend` 函数 `1` 次, 则参数为一个假设的 `int` 值, 最终返回结果为一个
      `int` 列表, 且长度为 `2`, 即 `[n1, n2]`;
    - 如果调用 `extend` 函数 `3` 次, 则参数可能为一个 `int` 值, 或者为一个长度为 `2` 的
      列表, 所以最终返回结果为 `[n1, n2, n3]` 或 `[[n1, n2], n3]` 或
      `[n1, [n2, n3]]`

    """
    # 确认参数的类型为 List 或 int
    assert isinstance(r, (List, int))

    if isinstance(r, List):
        # 对于参数类型为 List 类型, 确认列表的最大长度
        assert 1 <= len(r) <= 10

        # 遍历列表
        for n in r:
            # 列表元素类型为 int 或 List 集合
            assert isinstance(n, (List, int))

            if isinstance(n, int):
                # 如果元素类型为 int, 则确认整数范围
                assert 1 <= n <= 10
            elif isinstance(n, List):
                # 如果元素类型为 List, 则确认集合长度范围
                assert len(n) == 2
    elif isinstance(r, int):
        # 对于参数类型为 int 类型, 确认整数的范围
        assert 1 <= r <= 10


@given(
    n=st.sampled_from(list(range(100)))
    .filter(lambda n: n % 2 == 0)
)
def test_strategies_sampled_from(n: int) -> None:
    """
    从一个集合中每次选择一个用例, 并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.sampled_from(elements)
    ```
    """
    # 确认参数类型为所给集合元素类型
    assert isinstance(n, int)
    # 确认参数值符合过滤器条件
    assert n % 2 == 0
    # 确认符合假设数据的范围
    assert 0 <= n < 100


@given(s=st.sets(
    elements=st.integers(min_value=1, max_value=100),
    min_size=1,
    max_size=10,
))
def test_strategies_sets(s: Set[int]) -> None:
    """
    假设一组 `Set` 集合对象, 并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.sets(
        elements,       # Set 集合元素类型
        *,
        min_size=0,     # 集合最小长度
        max_size=None   # 集合最大长度
    )
    ```
    """
    # 确认参数类型为 Set 类型
    assert isinstance(s, Set)
    # 确认 Set 集合元素长度为
    # 确认 Set 集合中元素为 int 类型
    assert all([isinstance(n, int) for n in s])

    # 确认集合元素取值范围
    assert all([1 <= n <= 100 for n in s])


def test_strategies_shared() -> None:
    """
    返回一个假设对象, 该对象基于其 `base` 参数定义的假设对象, 产生一个共享的测试用例值.
    任意两个具备相同 `key` 参数的 `shared` 假设对象将共享相同的值. 否则将自动使用当前假设
    的标识作为 `key`, 其定义如下:

    ```
    hypothesis.strategies.shared(
        base,       # 基本的假设对象, shared 假设对象将基于此对象产生用例
        *,
        key=None    # 标识字符串
    )
    ```
    """
    s = st.integers(min_value=1)

    v1 = st.shared(base=s)
    assert type(s.example()) == type(v1.example())  # noqa

    v2 = st.shared(base=s)
    assert type(v1.example()) == type(v2.example())  # noqa

    v1 = st.shared(base=s, key="h1")
    v2 = st.shared(base=s, key="hi")
    assert type(v1.example()) == type(v2.example())  # noqa


@given(
    s=st.slices(size=10)
    .filter(lambda s: s.start is not None)  # 过滤掉非正常 slice 取值的情况
    .filter(lambda s: s.stop is not None)
    .filter(lambda s: s.step is not None)
)
def test_strategies_slices(s: Any) -> None:
    """
    根据设定的集合长度, 假设一组切片对象, 传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.slices(size)  # size 表示对应的集合最大长度
    ```

    本例中, 假设能在长度为 `10` 的集合上进行切片操作的切片对象, 所以改切片对象的 `start`,
    `stop` 和 `step` 属性会在设置的集合长度范围内随机变化
    """
    # 确定参数类型为切片类型
    assert isinstance(s, slice)

    # 产生一个长度为 10 的列表集合对象
    ns = list(range(1, 11))

    # 通过假设的切片对象获取子集合
    sub = ns[s]
    assert len(sub) < len(ns)


@given(s=st.text(
    alphabet="abcde",  # 从 abcde 这个序列中产生字符组成最终的测试用例
    min_size=1,
    max_size=10,
))
def test_strategies_text(s: str) -> None:
    """
    假设一组字符串并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.text(
        alphabet=characters(blacklist_categories=('Cs',)), # 组成字符串的字符假设
            # 规则. 该参数可以为一个字符序列或者一个字符串假设对象, 最终产生的字符串的各
            # 个字符会在参数指定的字符范围内随机产生
        *,
        min_size=0,    # 字符串的最小长度
        max_size=None  # 字符串的最大长度
    )
    ```

    本例中假设了一组由 `abcde` 字母组成的长度在 `1` ~ `10` 之间的字符串
    """
    # 确认参数类型为字符串类型
    assert isinstance(s, str)

    # 确认字符串的字符组成
    assert re.match("^[a-e]+$", s)

    # 确认字符串长度限定范围
    assert 1 <= len(s) <= 10


@given(dt=st.timedeltas(
    min_value=timedelta(days=1, hours=1, minutes=1),
    max_value=timedelta(days=2, hours=2, minutes=2),
))
def test_strategies_timedeltas(dt: timedelta) -> None:
    """
    假设一组时差对象并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.timedeltas(
        min_value=datetime.timedelta.min, # 时差允许的最小值
        max_value=datetime.timedelta.max  # 时差允许的最大值
    )
    ```
    """
    # 确认参数类型为时差对象类型
    assert isinstance(dt, timedelta)

    # 确认时差对象的取值范围在规定范围内
    assert (
        timedelta(days=1, hours=1, minutes=1)
        <= dt
        <= timedelta(days=2, hours=2, minutes=2)
    )


@given(t=st.times(
    min_value=time(1, 0, 0),
    max_value=time(12, 59, 59),
    timezones=st.timezones(),  # 允许为生成的时间假设时区
))
def test_strategies_times(t: time) -> None:
    """
    假设一组时间对象并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.times(
        min_value=datetime.time.min,  # 允许的最小值
        max_value=datetime.time.max,  # 允许的最大值
        *,
        timezones=none()  # 生成时区的假设对象
    )
    ```
    """
    # 确保参数类型为时间类型
    assert isinstance(t, time)

    # 确保假设的时间对象带有时区信息
    assert t.tzinfo is not None

    # 去掉时区信息, 确保假设的时间对象在指定的范围内
    t = t.replace(tzinfo=None)
    assert time(1, 0, 0) <= t <= time(12, 59, 59)


@given(tz=st.timezone_keys(
    allow_prefix=True,  # 允许时区前缀
))
def test_strategies_timezone_keys(tz: str) -> None:
    """
    假设一组时区名称并传递给测试参数, 其定义如下:

    ```
    hypothesis.strategies.timezone_keys(
        *,
        allow_prefix=True  # 时区名称允许添加前缀
    )
    ```
    """
    # 确保参数为字符串类型, 表示一个时区名称
    assert isinstance(tz, str)

    # 过滤特殊的时区名称
    assume(not tz.startswith("posix"))
    assume(not tz.startswith("right"))
    assume(tz != "localtime")
    assume(tz != "Factory")

    # 确认假设的时区是有效时区
    assert tz in pytz.all_timezones


@given(tz=st.timezones())
def test_strategies_timezones(tz: tzinfo) -> None:
    """ # noqa
    假设一组时区类型 (`tzinfo`) 对象并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.timezones(
        *,
        no_cache=False  # 如果设置为 True, 会在 tzinfo 构造器中传递
                        # ZoneInfo.no_cache 参数, 可能会在产生时区对象时产生一些意外
                        # 情况. 参考: https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo.no_cache
    )
    ```
    """
    # 确认参数类型为 tzinfo 类型
    assert isinstance(tz, tzinfo)

    # 获取时区名称
    tz_name = str(tz)

    # 过滤特殊的时区名称
    assume(not tz_name.startswith("posix"))
    assume(not tz_name.startswith("right"))
    assume(tz_name != "localtime")
    assume(tz_name != "Factory")

    # 确认假设的时区是有效时区
    assert tz_name in pytz.all_timezones


@given(t=st.tuples(
    st.integers(),
    st.integers(),
    st.booleans(),
    st.text(min_size=1),
))
def test_strategies_tuples(t: Tuple[int, int, bool, str]) -> None:
    """
    假设一组 `Tuple` 对象并传入测试参数, 其定义如下:

    ```
    hypothesis.strategies.tuples(*args)
    ```

    `*args` 参数是一组假设器, 用于假设 `Tuple` 对象的每一个元素
    """
    # 确认参数类型
    assert isinstance(t, tuple)

    # 确认参数长度
    assert len(t) == 4

    # 确认每个元素的类型
    assert isinstance(t[0], int)
    assert isinstance(t[1], int)
    assert isinstance(t[2], bool)
    assert isinstance(t[3], str)
