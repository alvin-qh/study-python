####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from typing import cast

import camera
from draw_model import draw_model
from teapot import load_triangles
from transforms import stretch
from vectors import Polygons

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.16_slant_teapot", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将每个向量的 x 轴分量拉伸 4 倍
slanted_triangles = [
    [stretch(vertex, sx=vertex[1]) for vertex in triangle]
    for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, slanted_triangles))
