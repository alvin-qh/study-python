from typing import Tuple, Union

# 定义一个数类型
Number = Union[int, float]

# 表示一个二维向量
Vector2D = Tuple[Number, Number]

# 表示一个极坐标
Polar = Tuple[Number, Number]

# 表示一个三维向量
Vector3D = Tuple[Number, Number, Number]

# 表示一个 N 维向量
Vector = Tuple[Number, ...]

# 表示一个面
Face = Tuple[Vector3D, Vector3D, Vector3D]
