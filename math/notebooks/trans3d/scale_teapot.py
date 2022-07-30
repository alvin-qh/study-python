####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from typing import cast

import camera
from draw_model import draw_model
from teapot import load_triangles
from vectors import Polygons, scale

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.5_scale_teapot", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将模型中的每个三角形放大 2 倍
scaled_triangles = [
    [scale(vertex, 2.0) for vertex in triangle]
    for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, scaled_triangles))
