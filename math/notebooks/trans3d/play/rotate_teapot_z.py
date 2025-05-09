####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import math
import sys

from utils.draw import camera
from utils.draw.model import draw_model
from utils.draw.teapot import load_model
from utils.transform import rotate_z
from utils.vector import as_polygons

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.12_rotate_teapot_z", [0])

# 读取茶壶模型
original_triangles = load_model()

# 将模型的每个向量围绕 z 轴旋转 45°
rotated_triangles = as_polygons(
    [rotate_z(math.pi / 4, vertex) for vertex in triangle]
    for triangle in original_triangles
)

# 绘制茶壶模型
draw_model(rotated_triangles)
