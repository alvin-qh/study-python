####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from typing import cast

import camera
from draw_model import draw_model
from teapot import load_triangles
from vectors import Polygons, add, scale

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig4.6_scale_translate", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 要移动的偏移向量
offset = (-1, 0, 0)

# 将模型中的每个向量放大 2 倍后沿 x 轴负方向移动 1 个单位
scaled_triangles = [
    [add(offset, scale(vertex, 2.0)) for vertex in triangle]
    for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, scaled_triangles))
