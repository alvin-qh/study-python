####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import math
import sys

from common.transform import rotate_x
from common.vector import as_polygons
from draw import camera
from draw.model import draw_model
from draw.teapot import load_model

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.11_rotate_teapot_x", [0])

# 读取茶壶模型
original_triangles = load_model()

# 将模型的每个向量围绕 z 轴旋转 45°
rotated_triangles = as_polygons(
    [rotate_x(math.pi / 2, vertex) for vertex in triangle]
    for triangle in original_triangles
)

# 绘制茶壶模型
draw_model(rotated_triangles)
