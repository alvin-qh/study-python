# 演示颜色相关的测试用例提供者
import re

from faker import Faker

fake = Faker()

# HSV 色彩空间: HSV 色彩空间由三个值组成, 分别为:
#   H (Hue, 色调): 表示色彩信息, 即所处的光谱颜色的位置. 该参数用一角度量来
#                  表示红, 绿, 蓝分别相隔 120 度. 互补色分别相差 180 度
#   S (Saturation, 饱和度): 为一比例值, 范围从 0 到 1, 表示成所选颜色的纯度
#                           和该颜色最大的纯度之间的比率. S = 0 时只有灰度
#   V (Value, 明亮度): 表示色彩的明亮程度, 范围从 0 到 1, 有一点要注意: 它
#                      和光强度之间并没有直接的联系


def test_provider_color() -> None:
    """
    产生一组色值相关的测试用例, 其定义如下:

    ```
    color(
        hue: Optional[HueType] = None,
        luminosity: Optional[str] = None,
        color_format: str = 'hex'
    ) -> str
    ```

    `color(...)` 函数先产生一个 `HSV` 色彩空间的色值, 之后转化为 `color_format` 参数定
    义的色值

    其中:
    - `hue` 参数, 定义 `HSV` 色彩空间的 `H` 值, 可以为 `str` 类型, `int` 类型或者
      `Tuple[int, int]` 类型
        - `str` 类型, 为一个颜色名 (例如 `"red"`, `"blue"` 等), 将在指定的颜色范围内
          随机选择一个值作为 `H` 值
        - `int` 类型, 表示 `H` 值的角度, 取值为 `0°`~`360°`
        - `Tuple[int, int]` 类型, 表示一个角度的范围, `H` 值将在此范围内随机选择
    - `luminosity` 参数用于控制 `S` 和 `V` 值选取的情况, 可以取值为: `"bright"`,
      `"dark"`, `"light"` 和 `"random"`
    - `color_format` 参数指定返回数据的类型, 可以取值为: `"hsv"`, `"hsl"`, `"rgb"`
      和 `"hex"` (默认值)
    """
    # 产生一个随机的红色系颜色, 结果以 16 进制格式返回
    value = fake.color(hue="red")
    # 确认返回的是 #rrggbb
    assert re.match(r"^#([a-z0-9]{2}){3}$", value)

    # 产生一个随机的65°, 偏淡的颜色, 结果以 16 进制格式返回
    value = fake.color(hue=65, luminosity="light")
    # 确认返回的是 #rrggbb
    assert re.match(r"^#([a-z0-9]{2}){3}$", value)

    # 产生一个随机的65°, 偏淡的颜色, 结果以 rgb 格式返回
    value = fake.color(hue=(100, 200), color_format="rgb")
    # 确认返回的是 rgb(r, g, b) 格式的结果
    assert re.match(r"^rgb\((,?\s*\d{1,3}){3}\)$", value)

    # 产生一个颜色, 结果以 hsv 格式返回
    value = fake.color(color_format="hsv")
    # 确认返回的是 rgb(r, g, b) 格式的结果
    assert re.match(r"^hsv\((,?\s*\d{1,3}){3}\)$", value)

    # 产生一个颜色, 结果以 hsl 格式返回
    value = fake.color(color_format="hsl")
    # 确认返回的是 rgb(r, g, b) 格式的结果
    assert re.match(r"^hsl\((,?\s*\d{1,3}){3}\)$", value)


def test_provider_color_name() -> None:
    """
    产生一个颜色名称, 其定义如下:

    ```
    color_name(
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> str
    ```

    其中:
    - `min_length` 参数, 颜色名的最小长度
    - `max_length` 参数, 颜色名的最大长度

    颜色名是一组英文单词, 用来描述颜色, 并不特指计算机系统的颜色名称, 例如: BlueViolet,
    Chocolate, Snow 等
    """
    value = fake.color_name(min_length=3)
    # 确认生成的颜色名称长度
    assert len(value) >= 3


def test_provider_hex_color() -> None:
    """
    产生一个 16 进制格式的色值, 其定义如下:

    ```
    hex_color() -> str
    ```

    返回一个格式为 `#rrggbb` 的色值
    """
    value = fake.hex_color()
    # 确认结果符合 #rrggbb 格式
    assert re.match(r"^#([a-z0-9]{2}){3}$", value)


def test_provider_rgb_color() -> None:
    """
    产生一个 rgb 格式的色值, 其定义如下:

    ```
    rgb_color() -> str
    ```

    返回一个格式为 `rr,gg,bb` 的色值
    """
    value = fake.rgb_color()
    # 确认结果符合 rr,gg,bb 格式
    assert re.match(r"(,?\d{1,3}){3}", value)


def test_provider_rgb_css_color() -> None:
    """
    产生一个 css rgb 格式的色值, 其定义如下:

    ```
    rgb_css_color() -> str
    ```

    返回的格式为 `rgb(rr,gg,bb)` (注意, `,` 后没有空格) 的色值
    """
    value = fake.rgb_css_color()
    # 确认返回结果为 rgb(rr,gg,bb) 格式
    assert re.match(r"^rgb\((,?\d{1,3}){3}\)$", value)


def test_provider_safe_color_name() -> None:
    """
    产生一个 web-safe 的颜色名, 其定义如下:

    ```
    safe_color_name(
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> str
    ```

    其中:
    - `min_length` 参数, 颜色名的最小长度
    - `max_length` 参数, 颜色名的最大长度
    """
    value = fake.safe_color_name()
    # 颜色名全部为小写字母
    assert re.match(r"^[a-z]+$", value)


def test_provider_safe_hex_color() -> None:
    """
    产生一个 web-safe 的 16 进制色值, 其定义如下:

    ```
    safe_hex_color() -> str
    ```
    """
    value = fake.safe_hex_color()
    assert re.match(r"#([a-z0-9]){3}", value)
