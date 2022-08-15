import re
from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from typing import Any, Dict, Tuple, TypeVar
from xmlrpc.client import Boolean

from hypothesis import assume, given, note
from hypothesis import strategies as st


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
    unit=st.sampled_from(["mm", "cm", "m", "km"]),  # 为 format_num 函数假设的第二个参数
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

    备注: 所谓 Unicode 类别, 即对 Unicode 字符的一个分类, 具体参考 https://unicodeplus.com/category
    和 https://wikipedia.org/wiki/Unicode_character_property

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
        allow_subnormal=True # 是否允许非规格化浮点数, 参考: https://en.wikipedia.org/wiki/Subnormal_number
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
def element_and_index(draw: st.DrawFn, element: st.SearchStrategy[E]) -> Tuple[int, E]:
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

    注意: 这并不是意味着要把后一个假设的值用于前一个假设, 而是通过后一个假设定义为前一个假设产生值,
    所以两个假设的值并不相同
    """
    # 假设 a 引用假设 b, 此时假设 b 尚未定义
    a = st.deferred(lambda: b)

    # 再假设 a 后定义假设 b
    b = st.integers()

    # 确定假设 a 通过假设 b 产生值
    assert isinstance(a.example(), int)


@given(d=st.dictionaries(
    keys=st.from_regex(r"[a-z]{3}", fullmatch=True),  # 假设任意三个字母作为 key
    values=st.integers(min_value=1, max_value=100),  # 假设任意 1~100 整数作为 value
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
        allow_subnormal=None, # 是否允许非规格化浮点数, 参考: https://en.wikipedia.org/wiki/Subnormal_number
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
    regex=r"(13[0-9]|14[579]|15[0-35-9]|16[6]|17[0135678]|18[0-9]|19[89])[0-9]{8}",
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
    注意: `\d` 会产生各类 Unicode 字符的数字 (例如罗马数字), 所以不能简单的用 `\d`, 
    而是 `[0-9]`, 限定为阿拉伯数字
    """
    assert len(s) == 11
    assert s[0] == "1"


@given(t=st.from_type(thing=int))
def test_strategies_from_type(t: Any) -> None:
    """
    """
    assert isinstance(t, int)
