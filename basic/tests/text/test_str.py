from itertools import repeat
from string import Template
from typing import Any, Callable, Optional


def test_ascii_convert() -> None:
    """测试将字符和 ASCII 码之间的互相转换"""

    # 字符转为 ASCII 码
    assert ord("A") == 65
    # ASCII 码转为字符
    assert chr(97) == "a"

    # 将字符串内容转为 ASCII 编码表示

    # ASCII 字符转为 ASCII 编码表示
    assert ascii("AB") == "'AB'"
    # UNICODE 字符转为 ASCII 编码表示
    assert ascii("测试") == "'\\u6d4b\\u8bd5'"


def test_str_slice() -> None:
    """字符串切片操作"""

    s = "一二三四五六七八九零"

    # 通过下标获取指定位置嗯字符
    assert s[2] == "三"
    # 获取一个范围的切片
    assert s[1:4] == "二三四"
    # 获取指定位置到结尾的切片
    assert s[2:] == "三四五六七八九零"
    # 获取开头到指定位置的切片
    assert s[:3] == "一二三"
    # 位置可以使用负数, 表示从字符串末尾倒数计算
    assert s[-4:] == "七八九零"
    # 设置切片的步长
    assert s[1:-1:2] == "二四六八"

    # 利用 LC 切片发获取每字符串两个字符的集合
    fivers = [s[k : k + 2] for k in range(0, len(s), 2)]
    assert fivers == ["一二", "三四", "五六", "七八", "九零"]

    cuts = [2, 5, 9]
    # 将首位, 末尾位置加上后, 产生 2 元组序列
    # 相当于 zip([0, 2, 5, 9], [2, 5, 9, 10])
    slices = list(zip([0] + cuts, cuts + [len(s)]))
    assert slices == [(0, 2), (2, 5), (5, 9), (9, 10)]
    # 进行切片
    fivers = [s[i:j] for i, j in slices]
    assert fivers == ["一二", "三四五", "六七八九", "零"]


def test_str_multiplication() -> None:
    """字符串的乘法操作, 相当于将字符串内容重复多次后形成新的字符串"""

    s = "xo"
    # 验证重复 3 次的结果
    assert s * 3 == "xoxoxo"


def test_character_filter() -> None:
    """`str` 用于字符过滤判断的函数包括:

    - `isdigit` 返回字符串是否全部由数字字符组成
    - `isalpha` 返回字符串是否全部由字母 (或汉字) 字符组成
    - `isalnum` 结果相当于 `isalpha` 和 `isdigit` 两个函数的组合
    """

    # 判断字符串是否全部为数字字符
    assert "123".isdigit() is True
    assert "a23".isdigit() is False

    # 判断字符串是否全部为字母字符
    assert "123".isalpha() is False
    assert "abc".isalpha() is True

    # 判断字符串是否全部为数字+字母字符
    assert "123".isalnum() is True
    assert "abc".isalnum() is True
    assert "a1b2c3".isalnum() is True
    assert "_1c".isalnum() is False


def test_counter() -> None:
    """`count` 方法用于计算字符串中子字符串出现的次数"""

    s = "abcdabcdabc"

    # 计算字符串中字符个数
    assert s.count("") == 12
    # 计算指定字符的个数
    assert s.count("b") == 3
    # 计算指定子字符串的个数
    assert s.count("bc") == 3
    # 查找 "bcd" 子字符串出现的次数, 并指定查找的起始位置和结束位置
    assert s.count("bcd", 2, -1) == 1


def test_split() -> None:
    """字符串分割

    `split` 方法和 `splitlines` 方法可以对字符串进行不同方式的分割
    """
    s = """a b
c
d
e"""

    # 默认情况下 split 方法根据空白字符串 (" ", "\t", "\n" 等) 分割字符串
    assert s.split() == ["a", "b", "c", "d", "e"]

    # 指定以换行符分割字符串
    assert s.split("\n") == ["a b", "c", "d", "e"]

    # 指定以换行符分割字符串
    assert s.splitlines() == ["a b", "c", "d", "e"]


def test_reversed() -> None:
    """反转字符串

    字符串本质上是一个字符的列表集合, 所以可以通过 "切片运算" 和 "`reversed` 函数" 两种方式进行反转
    """
    s = "abc def"

    # 通过切片反转字符串
    assert s[::-1] == "fed cba"
    # 通过 reversed 函数反转字符串
    assert "".join(reversed(s)) == "fed cba"

    # 将字符串切分后诸部份反转
    r = " ".join([e[::-1] for e in s.split(" ")])
    assert r == "cba fed"


def test_translate() -> None:
    """可以通过一个字符编码的字典对象, 对字符串中的指定字符进行转换

    - `maketrans` 方法用于通过简单方法形成转换字典
    - `translate` 方法用于执行转换
    """
    # 形成转换表, 将两个参数进行逐字符对应, 形成一个字典对象
    tab = str.maketrans("ABC", "abc")

    # 确认形成的转换表是正确的字典对象
    assert tab == {
        ord("A"): ord("a"),
        ord("B"): ord("b"),
        ord("C"): ord("c"),
    }

    # 对字符串进行转换
    s = "ABCDEF"
    # 确认转换结果
    assert s.translate(tab) == "abcDEF"


def test_format_by_c_like_style() -> None:
    """在 Python 2 中, 定义了一种类似 C 语言的字符串格式化语法

    格式化字符串和格式化参数通过 `%` 运算符分隔
    """
    s = "%s, %s, %s" % ("a", "b", "c")
    assert s == "a, b, c"


def test_format_by_method() -> None:
    """通过字符串对象的 `format` 方法进行字符串格式化

    `format` 方法通过一个模板字符串, 将字符串对象本身进行格式化, 返回格式化后的新字符串模板字符串中, `{}` 表示一个占位符,
    格式化时会用实际参数替换占位符
    """
    # 通过模板字符串进行格式化, 占位符会安装参数顺序依次被替换
    s = "{}, {}, {}".format("a", "b", "c")
    assert s == "a, b, c"

    # 在占位符中设置参数的位置
    # {0} 表示参数列表中的第一个参数  (即 "a"). 其它以此类推
    s = "{0}, {1}, {2}".format("a", "b", "c")
    assert s == "a, b, c"

    # 可以按任何参数顺序设定占位符
    s = "{2}, {1}, {0}".format("a", "b", "c")
    assert s == "c, b, a"

    # 可以重复使用某个参数位置的占位符
    s = "{0}{1}{0}".format("abra", "cad")
    assert s == "abracadabra"


def test_format_by_method_with_named_args() -> None:
    """可以通过命名参数的名称作为占位符的标识

    这种方式比使用位置占位符更加明确一些
    """
    # 占位符使用 latitude 和 longitude 两个命名参数
    # 在 format 方法中传入对应的命名参数即可进行格式化
    s = "{latitude}, {longitude}".format(latitude="37.24N", longitude="-115.81W")
    assert s == "37.24N, -115.81W"


def test_format_by_method_for_numbers() -> None:
    """在占位符中通过 `:<l>` 可以指定数字格式化的参数

    可用的参数包括:
    - `b` 数字格式化为二进制
    - `o` 数字格式化为 8 进制
    - `x` 数字格式化为 16 进制
    - `f` 数字格式化为 浮点数
    - `,` 数字按每三位一个部分分隔, 分隔符为 `,`
    - `%` 显示百分比, 即

    对于数字的符号, 有如下格式定义
    - `+`: 一定显示符号, 正数为 `+`, 负数为 `-`
    - `-`: 按需显示符号, 正数不显示, 负数为 `-`, 这个规则是默认规则

    数字长度
    - `n` `n` 表示数字的长度, 如果 n 大于数字本身的长度, 则用空格补足
    - `.n` `n` 表示保留的小数位数, 如果小数位小于 `n`, 则用 `0` 补足

    复数
    - `real` 实部
    - `imag` 虚部
    """
    # 格式化为二进制
    s = "{:b}".format(3)
    assert s == "11"

    # 格式化为八进制
    s = "{:o}".format(10)
    assert s == "12"

    # 格式化为 16 进制
    s = "{:x}".format(10)
    assert s == "a"

    # 格式化为每三位分段
    s = "{:,}".format(1234567890)
    assert s == "1,234,567,890"

    # 强制使用正负号
    s = "{:+f}, {:+f}".format(3.14, -3.14)
    assert s == "+3.140000, -3.140000"

    # 按需使用正负号
    s = "{:-f}, {:-f}".format(3.14, -3.14)
    assert s == "3.140000, -3.140000"

    # 按需在数字前增加空格 (如果之前没有空格, 则增加空格)
    s = "{: f}, {: f}".format(3.14, -3.14)
    assert s == " 3.140000, -3.140000"

    # 设置数字长度, 用空格补足
    s = "{:3}, {:3}".format(12, 123)
    assert s == " 12, 123"

    # 设置数字长度, 用 0 补足
    s = "{:03}, {:03}".format(12, 123)
    assert s == "012, 123"

    # 保留小数位, 如果不足则用 0 补足
    s = "{:.3f}, {:.1f}".format(3.14, -3.14)
    assert s == "3.140, -3.1"

    # 格式化为百分数
    s = "{:.2%}".format(19.5 / 22)
    assert s == "88.64%"

    # 在模板中指定复数的实部和虚部
    c = 3 - 5j
    s = "{0.real}, {0.imag}".format(c)
    assert s == "3.0, -5.0"
    s = "{c.real}, {c.imag}".format(c=c)
    assert s == "3.0, -5.0"


def test_format_by_method_for_list_index() -> None:
    """在模板字符串中, 可以在占位符中使用下标, 来输出一个列表集合 (List, Tuple) 的指定元素"""

    coord = [(3, 5), (6, 8)]

    # 参数 *coord 表示将 coord 变量拆为 2 个参数, 0 = (3, 5) 和 1 = (6, 8)
    # 所以 0[0] 表示 3, 0[1] 表示 5, 以此类推
    s = "({0[0]}, {0[1]}), ({1[0]}, {1[1]})".format(*coord)
    assert s == "(3, 5), (6, 8)"

    # 参数 coord 表示 0 = [(3, 5), (6, 8)]
    # 所以 0[0] 表示 (3, 5), 0[1] 表示 (6, 8)
    # 所以 0[0][0] 表示 3, 0[0][1] 表示 5, 以此类推
    s = "({0[0][0]}, {0[0][1]}), ({0[1][0]}, {0[1][1]})".format(coord)
    assert s == "(3, 5), (6, 8)"

    # 使用命名参数, c 表示列表集合参数
    s = "({c[0][0]}, {c[0][1]}), ({c[1][0]}, {c[1][1]})".format(c=coord)
    assert s == "(3, 5), (6, 8)"


class Value:
    """用于测试模板字符串中访问对象属性的类"""

    def __init__(self, id_: str, name: str) -> None:
        """初始化对象

        Args:
            - `id_` (`str`): 对象属性
            - `name` (`str`): 对象属性
        """
        self.id = id_
        self.name = name


def test_format_by_method_for_object_attributes() -> None:
    """可以在占位符中通过 `.<attribute name>` 访问对象的属性"""

    # 产生一个对象
    v = Value("001", "Alvin")

    # 在占位符中通过位置访问对象的属性
    s = "id={0.id}, name={0.name}".format(v)
    assert s == "id=001, name=Alvin"

    # 在占位符中通过命名参数访问对象的属性
    s = "id={v.id}, name={v.name}".format(v=v)
    assert s == "id=001, name=Alvin"


def test_format_by_method_for_dict_keys() -> None:
    """可以在占位符中通过 `[key]` 通过键访问字典的值"""

    data = {"id": "001", "name": "Alvin"}

    # 在占位符中通过位置访问字典的值
    s = "id={0[id]}, name={0[name]}".format(data)
    assert s == "id=001, name=Alvin"

    # 在占位符中通过命名参数访问字典的值
    s = "id={d[id]}, name={d[name]}".format(d=data)
    assert s == "id=001, name=Alvin"


def test_padding_align_and_fill() -> None:
    """在占位符中指定对齐方式和填充方式

    对齐方式可以指定为
    - `<n` 居左对齐, 内容居左, 右侧由填充符补齐
    - `>n` 居右对齐, 内容居右, 左侧由填充符补齐
    - `^n` 中央对齐, 左右两边由填充符补齐

    也可以在 `format` 方法中指定这些格式化参数
    """
    s = "{:<10}".format("A")
    assert s == "A         "

    s = "{:>10}".format("A")
    assert s == "         A"

    s = "{:^10}".format("A")
    assert s == "    A     "

    s = "{:*^10}".format("A")
    assert s == "****A*****"

    rs = []
    for align, text, n in zip("<^>", ["L", "C", "R"], repeat(5)):
        # 指定对齐方式和填充字符的参数
        rs.append("{:{f}{a}{n}}".format(text, f="*", a=align, n=n))
    # 确定格式化结果
    assert rs == [
        "L****",
        "**C**",
        "****R",
    ]


def test_use_str_templates() -> None:
    """`string` 包的 `Template` 类用于产生一个字符串模板对象

    通过字符串模板可以将一组参数格式化为字符串
    """
    # 实例化一个字符串模板, 模板中包含 arg 参数
    t = Template("This is $arg")

    # 通过设置一个包含 arg 键的字典对象, 将模板格式化为字符串
    s = t.substitute({"arg": "Alvin"})
    assert s == "This is Alvin"

    # 通过设置一个包含 arg 键的字典对象, 将模板格式化为字符串
    s = t.substitute({"arg": 123})
    assert s == "This is 123"


def test_format_magic_method() -> None:
    """一个类型的 `__format__` 魔法方法用于对该类的对象进行格式化

    当进行字符串格式化操作时 (`format`, `f""` 等), 如果参数对象具备 `__format__` 魔法方法, 则会调用该方法将对象格式化为字符串
    """

    class C:
        """测试对象格式化的类型"""

        # 格式化规则和格式化函数的对应关系
        _format = {
            "m": lambda v: "m" + str(v),
            "n": lambda v: "n" + str(v),
        }

        def __init__(self, value: Any) -> None:
            """初始化当前对象

            Args:
                - `value` (`Any`): 任意值
            """
            self._value = value

        def __format__(self, format_spec: str) -> str:
            """根据一个格式化规则格式化字符串

            Args:
                - `format_spec` (`str`): 格式化规则

            Returns:
                `str`: 格式化结果
            """
            # 根据格式化规则获取格式化函数
            formatter: Optional[Callable[..., str]] = self._format.get(format_spec)
            # 对于无效的格式化规则, 返回当前值
            if not formatter:
                return str(self._value)

            # 返回格式化后的值
            return formatter(self._value)

    c = C(123)

    # 验证格式化结果
    assert f"{c:m}" == "m123"
    assert f"{c:n}" == "n123"
    assert f"{c:x}" == "123"
