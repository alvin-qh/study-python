####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys
from math import pi
from typing import cast

from common.transform import rotate_z
from common.typedef import Polygons
from draw import camera
from draw.model import draw_model
from draw.teapot import load_triangles

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.12_rotate_teapot_z", [0])

# 读取茶壶模型
original_triangles = load_triangles()

# 将模型的每个向量围绕 z 轴旋转 45°
rotated_triangles = [
    [rotate_z(pi / 4, vertex) for vertex in triangle] for triangle in original_triangles
]

# 绘制茶壶模型
draw_model(cast(Polygons, rotated_triangles))
