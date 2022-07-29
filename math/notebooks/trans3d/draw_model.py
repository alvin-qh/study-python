from typing import Callable, Iterable, Optional, Tuple

import camera
import matplotlib.cm
import OpenGL.GL as gl
import OpenGL.GLU as glu
import pygame as game
from matplotlib.colors import Colormap
from transforms import multiply_matrix_vector, polygon_map
from vectors import Face, Matrix, Vector3D, cross, dot, subtract, unit


def normal(face):
    return(cross(subtract(face[1], face[0]), subtract(face[2], face[0])))


def shade(face, color_map: Optional[Colormap] = None, light=(1, 2, 3)):
    if not color_map:
        color_map = matplotlib.cm.get_cmap("Blues")  # type: ignore

    return color_map(1 - dot(unit(normal(face)), unit(light)))


def gl_axes():
    axes = [
        [(-1000, 0, 0), (1000, 0, 0)],
        [(0, -1000, 0), (0, 1000, 0)],
        [(0, 0, -1000), (0, 0, 1000)],
    ]
    gl.glBegin(gl.GL_LINES)

    for axis in axes:
        for vertex in axis:
            gl.glColor3fv((1, 1, 1))
            gl.glVertex3fv(vertex)

    gl.glEnd()


def draw_model(
        faces: Iterable[Face],
        color_map: Optional[Colormap] = None,
        light: Vector3D = (1, 2, 3),
        gl_rotatef_args: Optional[Tuple[float, float, float, float]] = None,
        get_matrix: Callable[[int], Matrix] = None,
) -> None:
    # 初始化引擎
    game.init()

    # 设置视窗显示模式
    win = game.display.set_mode(
        (400, 400),  # 窗口大小
        game.DOUBLEBUF | game.OPENGL,  # 显示属性
    )

    # 获取相机
    cam = camera.default_camera
    # 设置相机视窗
    cam.set_window(win)

    glu.gluPerspective(45, 1, 0.1, 50.0)
    gl.glTranslatef(0.0, 0.0, -5)

    if gl_rotatef_args:
        gl.glRotatef(*gl_rotatef_args)

    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glCullFace(gl.GL_BACK)

    while cam.is_shooting():
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                quit()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl_axes()

        gl.glBegin(gl.GL_TRIANGLES)

        def do_matrix_transform(v: Vector3D):
            if get_matrix:
                m = get_matrix(game.time.get_ticks())
                return multiply_matrix_vector(m, v)  # type: ignore

            return v

        transformed_faces = polygon_map(do_matrix_transform, faces)

        if not color_map:
            color_map = matplotlib.cm.get_cmap("Blues")  # type: ignore

        for face in transformed_faces:
            color = shade(face, color_map, light)
            for vertex in face:
                gl.glColor3fv((color[0], color[1], color[2]))
                gl.glVertex3fv(vertex)

        gl.glEnd()
        cam.tick()
        game.display.flip()
