####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot
import sys

from draw.model import draw_model
from draw.teapot import load_model
from draw import camera

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig_4.4_draw_teapot", [0])

# 绘制茶壶模型
draw_model(load_model())
