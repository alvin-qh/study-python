####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys

from common.transform import stretch
from common.vector import as_polygons
from draw import camera
from draw.model import draw_model
from draw.teapot import load_model

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.13_stretch_teapot_x", [0])

# 读取茶壶模型
original_triangles = load_model()

# 将每个向量的 x 轴分量拉伸 4 倍
stretched_triangles = as_polygons(
    [stretch(vertex, sx=4.0) for vertex in triangle] for triangle in original_triangles
)

# 绘制茶壶模型
draw_model(stretched_triangles)
