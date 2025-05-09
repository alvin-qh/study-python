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
    camera.default_camera = camera.Camera("fig_4.5_scale_teapot", [0])

# 读取茶壶模型
original_triangles = load_model()

# 将模型中的每个三角形放大 2 倍
scaled_triangles = as_polygons(
    [scale(2.0, vertex) for vertex in triangle] for triangle in original_triangles
)

# 绘制茶壶模型
draw_model(scaled_triangles)
