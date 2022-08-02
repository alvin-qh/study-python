####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from typing import cast

import camera
from draw_model import draw_model
from teapot import load_triangles
from vectors import Polygons
from transforms import cube_stretch

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.15_cube_teapot_y", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将每个向量的 x 值和 y 值相加, 得到 (x + y, y, z) 这样的向量
cubed_triangles = [
    [cube_stretch(vertex, dim=(0, 1, 0)) for vertex in triangle]
    for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, cubed_triangles))
