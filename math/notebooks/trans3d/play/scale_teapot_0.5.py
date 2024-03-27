####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from typing import cast

from common.typedef import Polygons
from common.vector import scale
from draw import camera
from draw.model import draw_model
from draw.teapot import load_triangles

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("MINIPROJ_4.3b", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将模型的每个向量统一乘以 0.5, 茶壶缩小到原本的 1 / 2
moved_triangles = [
    [scale(vertex, 0.5) for vertex in triangle] for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, moved_triangles))
