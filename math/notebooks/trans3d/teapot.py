# 从模型文件中加载数据
with open("teapot.off") as f:
    lines = f.readlines()

vertex_count, face_count, edge_count = map(int, lines[1].split())


def triple(xs):
    xs = list(xs)
    return (xs[0], xs[1], xs[2])


def load_vertices():
    vertices = []
    for i in range(2, 2+vertex_count):
        v = triple(map(float, lines[i].split()))
        vertices.append(scale_by(2)(rotate_x_by(-pi/2)
                        (translate_by((-0.5, 0, -0.6))(v))))
    return vertices
