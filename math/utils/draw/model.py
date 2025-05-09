from typing import Any, Callable, Optional, Sequence, Tuple

import matplotlib as mpl
import OpenGL.GL as gl
import OpenGL.GLU as glu
import pygame as game
from utils.transform import polygon_map
from utils.types import Matrix, Triangle, Vector3D
from utils.vector import (
    dot,
    multiply_matrix_vector,
    normal,
    unit,
)
from matplotlib.colors import Colormap

from utils.draw.camera import default_camera


_blues: Colormap = mpl.colormaps["Blues"]  # type: ignore


def shade(
    face: Triangle,
    color_map: Colormap = _blues,
    light: Vector3D = (1, 2, 3),
) -> Tuple[Any, ...] | Any:
    """计算 3D 图形的阴影色板

    Args:
        `face` (`Triangle`): 要绘制的三角形平面
        `color_map` (`Type[Colormap]`): 色板类型
        `light` (`Vector3D`): 入射光线向量

    Returns:
        `Tuple[Any, ...] | Any`: 颜色值
    """
    # 根据入射光线和平面法线的对齐程度, 计算颜色深浅
    return color_map(1 - dot(unit(normal(face)), unit(light)))


def gl_axes() -> None:
    """_summary_"""
    axes = [
        ((-1000, 0, 0), (1000, 0, 0)),
        ((0, -1000, 0), (0, 1000, 0)),
        ((0, 0, -1000), (0, 0, 1000)),
    ]
    gl.glBegin(gl.GL_LINES)

    for axis in axes:
        for vertex in axis:
            gl.glColor3fv((1, 1, 1))
            gl.glVertex3fv(vertex)

    gl.glEnd()


# glRotatef 函数参数类型
GlRotatefArgs = Tuple[float, float, float, float]


def draw_model(
    faces: Sequence[Triangle],
    color_map: Colormap = _blues,
    light: Vector3D = (1, 2, 3),
    gl_rotatef_args: Optional[GlRotatefArgs] = None,
    get_matrix: Optional[Callable[[int], Matrix]] = None,
) -> None:
    """绘制模型, 即有多面体组成的三维图形

    Args:
        `faces` (`Sequence[Triangle]`): 多面体模型
        `color_map` (Colormap, optional): 绘图用的色板. Defaults to `_blues`.
        `light` (`Vector3D`, optional): 光线向量. Defaults to `(1, 2, 3)`.
        `gl_rotatef_args` (`Optional[GlRotatefArgs]`, optional): `gl.glRotatef` 函数的参数. Defaults to `None`.
        `get_matrix` (`Optional[Callable[[int], Matrix]]`, optional): 获取向量矩阵的函数. Defaults to `None`.
    """
    # 初始化引擎
    game.init()

    # 设置视窗显示模式
    win = game.display.set_mode(
        (400, 400),  # 窗口大小
        game.DOUBLEBUF | game.OPENGL,  # 显示属性
    )

    # 获取相机
    cam = default_camera
    # 设置相机视窗
    cam.set_window(win)

    glu.gluPerspective(45, 1, 0.1, 50.0)
    gl.glTranslatef(0.0, 0.0, -5)

    if gl_rotatef_args:
        gl.glRotatef(*gl_rotatef_args)

    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glCullFace(gl.GL_BACK)

    def do_matrix_transform(v: Vector3D) -> Vector3D:
        if get_matrix:
            m = get_matrix(game.time.get_ticks())
            return multiply_matrix_vector(m, v)  # type: ignore

        return v

    while cam.is_shooting():
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                quit()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)  # type: ignore
        gl_axes()

        gl.glBegin(gl.GL_TRIANGLES)

        transformed_faces = polygon_map(do_matrix_transform, faces)

        if not color_map:
            color_map = mpl.cm.get_cmap("Blues")  # type: ignore

        for face in transformed_faces:
            color = shade(face, color_map, light)
            for vertex in face:
                gl.glColor3fv((color[0], color[1], color[2]))
                gl.glVertex3fv(vertex)

        gl.glEnd()
        cam.tick()
        game.display.flip()
