####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys

from utils.draw import camera
from utils.draw.model import draw_model
from utils.draw.teapot import load_model
from utils.transform import stretch
from utils.vector import as_polygons

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.13_stretch_teapot_x", [0])

# 读取茶壶模型
original_triangles = load_model()

# 将每个向量的 y 轴分量拉伸 4 倍
stretched_triangles = as_polygons(
    [stretch(vertex, sy=4.0) for vertex in triangle] for triangle in original_triangles
)

# 绘制茶壶模型
draw_model(stretched_triangles)
