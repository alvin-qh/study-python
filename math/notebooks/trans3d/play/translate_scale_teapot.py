####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys

from common.vector import add, as_polygons, scale
from draw import camera
from draw.model import draw_model
from draw.teapot import load_model

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("ex_translate_scale", [0])

# 读取茶壶模型
original_triangles = load_model()

# 要移动的偏移向量
offset = (-1, 0, 0)

# 将模型中的每个向量沿 x 轴负方向移动 1 个单位后放大 2 倍
scaled_triangles = as_polygons(
    [scale(2.0, add(offset, vertex)) for vertex in triangle]
    for triangle in original_triangles
)

# 绘制茶壶模型
draw_model(scaled_triangles)
