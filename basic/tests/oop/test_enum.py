from enum import Enum, Flag, IntEnum, auto
from typing import Any


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
    """测试获取所有枚举项"""

    class Color(Enum):
        """定义枚举类型"""

        RED = 1
        GREEN = 2
        BLUE = 3

    # 通过 list 函数获取枚类型的所有枚举项
    colors: Any = list(Color)
    assert colors == [Color.RED, Color.GREEN, Color.BLUE]

    colors = Color.__members__.values()
    assert list(colors) == [Color.RED, Color.GREEN, Color.BLUE]


def test_from_value_to_enum_item() -> None:
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    assert Color(1) == Color.RED
    assert Color(2) == Color.GREEN
    assert Color(3) == Color.BLUE


def test_from_name_to_enum_item() -> None:
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    assert Color["RED"] == Color.RED
    assert Color["GREEN"] == Color.GREEN
    assert Color["BLUE"] == Color.BLUE


def test_int_enum_class() -> None:
    class Color(IntEnum):
        RED = 1
        GREEN = 2
        BLUE = 3
        # YELLOW = "yellow"

    assert Color.RED.value == 1
    assert Color.GREEN.value == 2
    assert Color.BLUE.value == 3


def test_flag_enum_class() -> None:
    class Color(Flag):
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

    primary_colors = Color.RED | Color.GREEN | Color.BLUE
    secondary_colors = Color.YELLOW | Color.PURPLE | Color.ORANGE | Color.PINK
    gray_colors = Color.GRAY | Color.WHITE | Color.BLACK

    assert Color.RED in primary_colors
    assert Color.RED not in gray_colors
    assert Color.YELLOW not in primary_colors
    assert Color.YELLOW in secondary_colors
    assert Color.GRAY in gray_colors
