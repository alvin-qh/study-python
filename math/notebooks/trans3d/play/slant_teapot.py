####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from typing import cast

from common.typedef import Polygons
from common.vector import add
from draw import camera
from draw.model import draw_model
from draw.teapot import load_triangles

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.16_slant_teapot", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将每个向量的 x 轴分量拉伸 4 倍
slanted_triangles = [
    [add(vertex, (vertex[1], 0, 0)) for vertex in triangle]
    for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, slanted_triangles))
