####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys

from utils.draw import camera
from utils.draw.model import draw_model
from utils.draw.teapot import load_model
from utils.vector import as_polygons, scale

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("MINIPROJ_4.3b", [0])

# 读取茶壶模型
original_triangles = load_model()

# 将模型的每个向量统一乘以 -1, 相当于三个坐标轴全部翻转
moved_triangles = as_polygons(
    [scale(-1.0, vertex) for vertex in triangle] for triangle in original_triangles
)

# 绘制茶壶模型
draw_model(moved_triangles)
