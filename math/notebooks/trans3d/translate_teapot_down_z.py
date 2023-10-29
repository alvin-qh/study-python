####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from typing import cast

import camera
from draw_model import draw_model
from teapot import load_triangles
from vectors import Polygons, add

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("ex_translate_teapot_down_z", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将向量的 z 轴坐标减小 20 个单位, 绘制一个远离的茶壶
moved_triangles = [
    [add(vertex, (0, 0, -20)) for vertex in triangle]
    for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, moved_triangles))
