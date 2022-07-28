# 从模型文件中加载数据
from math import pi
from os import path

from transforms import rotate_x_by, scale_by, translate_by

with open(path.join(path.dirname(__file__), "teapot.off")) as f:
    lines = f.readlines()

vertex_count, face_count, edge_count = map(int, lines[1].split())


def triple(xs):
    xs = list(xs)
    return (xs[0], xs[1], xs[2])


def load_vertices():
    vertices = []

    for i in range(2, 2 + vertex_count):
        v = triple(map(float, lines[i].split()))

        f_scale = scale_by(2)
        f_rotate = rotate_x_by(-pi / 2)
        f_translate = translate_by((-0.5, 0, -0.6))

        vertices.append(f_scale(f_rotate(f_translate(v))))

    return vertices


def load_polygons():
    polys = []
    vertices = load_vertices()
    for i in range(2+vertex_count, 2+vertex_count+face_count):
        poly = list(map(vertices.__getitem__, map(int, lines[i].split()[1:])))
        polys.append(poly)
    return polys


def triangulate(poly):
    if len(poly) < 3:
        raise ValueError("polygons must have at least 3 vertices")

    for i in range(1, len(poly) - 1):
        yield (poly[0], poly[i+1], poly[i])


def load_triangles():
    tris = []
    polys = load_polygons()

    for poly in polys:
        for tri in triangulate(poly):
            assert(len(tri) == 3)

            for v in tri:
                assert(len(v) == 3)

            tris.append(tri)

    return tris
