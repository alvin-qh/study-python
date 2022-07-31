####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from math import pi
from typing import cast

import camera
from draw_model import draw_model
from teapot import load_triangles
from transforms import rotate_x
from vectors import Polygons

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.11_rotate_teapot_x", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将模型的每个向量围绕 z 轴旋转 45°
rotated_triangles = [
    [rotate_x(pi / 2, vertex) for vertex in triangle]
    for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, rotated_triangles))
