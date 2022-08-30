# 演示颜色相关的测试用例提供者
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

    `color` 先产生一个 `HSV` 色彩空间的
    """
