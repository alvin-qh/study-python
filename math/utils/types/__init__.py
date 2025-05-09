from typing import Sequence, Tuple, Union


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

# 表示一个三角形组成的平面 (三个三维向量组成)
Triangle = Tuple[Vector3D, Vector3D, Vector3D]

# 表示一个三维矩阵
Matrix3D = Sequence[Vector3D]

# 表示一个矩阵
Matrix = Sequence[Vector]
