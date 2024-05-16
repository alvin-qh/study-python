####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot

import sys

from common.transform import apply, polygon_map
from draw import camera
from draw.model import draw_model
from draw.teapot import load_model

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig4.35_linear_transform", [0])

# 绘制茶壶模型
draw_model(polygon_map(apply, load_model()))
