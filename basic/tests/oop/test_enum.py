from enum import Enum, Flag, IntEnum, auto


def test_enumeration_class() -> None:
    """测试枚举类型的使用

    当一个类从 `Enum` 类继承, 则该类表示为一个枚举类型, 枚举类型中可定义枚举项, 枚举项为当前枚举类型的一个实例

    每个枚举项都有一个名称和值, 并可通过枚举对象的 `name` 属性和 `value` 属性进行访问

    和其它类一样, 枚举类型中也可以定义方法和属性, 并可通过枚举项访问这些定义的方法与属性
    """

    class Color(Enum):
        """定义一个枚举类型

        该枚举类型中定义了三个枚举项, 以整数 `1`, `2` 和 `3` 为枚举值, 分别表示为 `RED`, `GREEN` 和 `BLUE` 三个枚举项
        """

        RED = 1
        GREEN = 2
        BLUE = 3

        def code(self) -> str:
            """在枚举类型中定义一个方法, 返回当前枚举项的名称和值"""
            return f"{self.name} {self.value}"

    # 确认枚举项的值和名称
    assert Color.RED.value == 1
    assert Color.RED.name == "RED"

    assert Color.GREEN.value == 2
    assert Color.GREEN.name == "GREEN"

    assert Color.BLUE.value == 3
    assert Color.BLUE.name == "BLUE"

    # 通过枚举项访问枚举中定义的方法
    assert Color.RED.code() == "RED 1"
    assert Color.GREEN.code() == "GREEN 2"
    assert Color.BLUE.code() == "BLUE 3"


def test_auto_increment_enum_item() -> None:
    """测试枚举值自增"""

    class Color(Enum):
        """定义一个枚举类型

        该枚举类型的枚举项为整数类型, 且只为第一个枚举项设置了具体的值, 之后的枚举项都通过 `auto` 函数生成,
        每个 `auto` 函数都会返回其前一个枚举项 `+1` 后的值
        """

        RED = 10  # 定义第一个枚举项的值
        GREEN = auto()  # 通过 auto 函数生成枚举项的值, 值为 11
        BLUE = auto()  # 通过 auto 函数生成枚举项的值, 值为 12

    # 确认枚举项的值和名称
    assert Color.RED.value == 10
    assert Color.RED.name == "RED"

    assert Color.GREEN.value == 11
    assert Color.GREEN.name == "GREEN"

    assert Color.BLUE.value == 12
    assert Color.BLUE.name == "BLUE"


def test_other_enum_value_type() -> None:
    """测试用其它类型作为枚举项的值

    除整数外, 还可以用其它类型作为枚举项的值, 比如字符串类型, 元组类型, 列表类型等等
    """

    class Color(Enum):
        """定义枚举类型

        该枚举类型的枚举项的值为字符串
        """

        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    # 确认各枚举项的值
    assert Color.RED.value == "red"
    assert Color.GREEN.value == "green"
    assert Color.BLUE.value == "blue"


def test_list_all_enum_items() -> None:
    """测试获取所有枚举项

    枚举类型本身可看作一个可迭代对象, 可以通过对枚举类型进行迭代, 来获取其包含的所有枚举项

    所以也可以通过 `in` 运算符判断某个枚举项是否为指定枚举的枚举项

    另外, 枚举类型的 `.__members__` 魔术成员属性的值为一个字典, Key 为枚举项的名称, Value 为枚举项实例, 通过该字典,
    也可以获取所有枚举项
    """

    class Color(Enum):
        """定义枚举类型"""

        RED = 1
        GREEN = 2
        BLUE = 3

    # 可通过 in 运算符判断某个枚举项是否为指定枚举的枚举项
    assert Color.RED in Color
    assert Color.GREEN in Color

    # Color 可看作一个可迭代对象, 通过 list 函数获取枚类型的所有枚举项
    colors = list(Color)
    assert colors == [Color.RED, Color.GREEN, Color.BLUE]

    # 通过 __members__ 魔术成员属性获取 Key 为枚举项名称, Value 为枚举项实例的字典,
    # 通过字典的 values 方法获取所有枚举项实例
    colors = list(Color.__members__.values())
    assert colors == [Color.RED, Color.GREEN, Color.BLUE]


def test_from_value_to_enum_item() -> None:
    """测试通过枚举项的值获取枚举项对象

    通过枚举类型构造器, 参数传入枚举项的值, 可以得到枚举项对象

    由于枚举项本身为单例对象, 故枚举类型构造器并不会创建新枚举项对象, 而是返回已经存在的枚举项对象
    """

    class Color(Enum):
        """定义枚举类型"""

        RED = 1
        GREEN = 2
        BLUE = 3

    # 确认通过枚举项的值可以获取枚举项对象
    assert Color(1) == Color.RED
    assert Color(2) == Color.GREEN
    assert Color(3) == Color.BLUE

    # 确认枚举项对象为单例, 对于指定枚举项, 无论通过什么方法, 得到的都是同一对象
    assert Color(1) is Color.RED
    assert Color(2) is Color.GREEN
    assert Color(3) is Color.BLUE


def test_from_name_to_enum_item() -> None:
    """测试通过枚举项名称获取枚举项对象

    枚举类型本身可以看作是一个字典, 故通过枚举项名称为 Key, 即可获取其对应的枚举项对象
    """

    class Color(Enum):
        """定义枚举类型"""

        RED = 1
        GREEN = 2
        BLUE = 3

    # 测试通过枚举项名称为 Key, 获取枚举项对象
    assert Color["RED"] == Color.RED
    assert Color["GREEN"] == Color.GREEN
    assert Color["BLUE"] == Color.BLUE


def test_int_enum_class() -> None:
    """测试整型枚举类型

    整数型枚举类型规定了枚举项的值必须为整数, 其余和普通枚举类型一致

    通过继承 `IntEnum` 类即可以创建整型枚举类型
    """

    class Color(IntEnum):
        """定义整型枚举类型

        所有枚举项的值必须为整数, 否则会报错
        """

        RED = 1
        GREEN = 2
        BLUE = 3
        # YELLOW = "yellow"  # 这里的枚举值不是整数, 故会报告错误

    # 确认枚举项的值
    assert Color.RED.value == 1
    assert Color.GREEN.value == 2
    assert Color.BLUE.value == 3


def test_flag_enum_class() -> None:
    """测试标志型枚举类型

    标志型枚举 (`Flag`) 类型本身是整数型枚举类型 (`IntEnum`), 但其重新定义了 `in` 运算符,
    使得 `in` 运算符可以通过按位 `&` 运算符判断多个枚举项是否为指定枚举的枚举项

    所以标志型枚举项的值应该为 `2` 的 `n` 次幂, 如: `1`, `2`, `4`, `8`, `16`, `32`, `64`, `128`, `256`, `512` 等,
    这些数字可以通过按位 `|` 运算符进行随意组合, 并在之后通过按位 `&` 运算符判断是否为指定枚举的枚举项, 其运算原理如下:

    ```python
    a, b, c, d, e = 1, 2, 4, 8, 16

    ab = a | b
    cd = c | d
    de = d | e
    abde = ab | de

    assert a & ab == a
    assert b & ab == b
    ```

    `Flag` 类型枚举内置了这个计算过程, 并将其简化为 `in` 运算符逻辑
    """

    class Color(Flag):
        """定义标志型枚举类型

        每个枚举项的值都为 `2` 的 `n` 次幂, 且不重复
        """

        RED = 1
        GREEN = 2
        BLUE = 4
        YELLOW = 8
        PURPLE = 16
        ORANGE = 32
        PINK = 64
        GRAY = 128
        WHITE = 256
        BLACK = 512

    # 通过 | 运算符定义多个枚举项组合结果
    primary_colors = Color.RED | Color.GREEN | Color.BLUE
    secondary_colors = Color.YELLOW | Color.PURPLE | Color.ORANGE | Color.PINK
    gray_colors = Color.GRAY | Color.WHITE | Color.BLACK

    # 确认可通过 in 运算符查询指定枚举项是否再某个枚举项组合中
    assert Color.RED in primary_colors
    assert Color.RED not in gray_colors
    assert Color.YELLOW not in primary_colors
    assert Color.YELLOW in secondary_colors
    assert Color.GRAY in gray_colors
