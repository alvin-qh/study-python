# 表示一个数值, 可以为整数或浮点数
from typing import Tuple, Union

# 定义一个数类型
Number = Union[int, float]

# 表示一个笛卡尔向量
Vector2D = Tuple[Number, Number]

# 表示一个极坐标向量
PolarVector = Tuple[Number, Number]

# 表示一个 3D 笛卡尔向量
Vector3D = Tuple[Number, Number, Number]
