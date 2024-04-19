import numpy as np
from timeit import default_timer as timer


class Triangle:
    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray):
        self.vs = np.array([a, b, c])
        v1 = b - a
        v2 = c - a
        cr = np.cross(v1[0:3], v2[0:3])
        n = cr / np.linalg.norm(cr)
        self.normal = np.append(n, 1)


class Object3d:
    def __init__(self, mesh: list[Triangle], pos: np.ndarray, scale: np.ndarray = np.array([1, 1, 1, 1])):
        self.pos = pos
        self.scale = scale

        self.meshM = []
        self.normalM = []
        for t in mesh:
            self.meshM.append(t.vs[0])
            self.meshM.append(t.vs[1])
            self.meshM.append(t.vs[2])
            self.normalM.append(t.normal)

        self.meshM = np.array(self.meshM)
        self.normalM = np.array(self.normalM)


def make_cube() -> Object3d:
    mesh = [
        # # front
        Triangle(np.array([-0.5, -0.5, -0.5, 1]), np.array([-0.5, 0.5, -0.5, 1]), np.array([0.5, 0.5, -0.5, 1])),
        Triangle(np.array([-0.5, -0.5, -0.5, 1]), np.array([0.5, 0.5, -0.5, 1]), np.array([0.5, -0.5, -0.5, 1])),

        # bot
        Triangle(np.array([0.5, -0.5, 0.5, 1]), np.array([-0.5, -0.5, 0.5, 1]), np.array([-0.5, -0.5, -0.5, 1])),
        Triangle(np.array([0.5, -0.5, 0.5, 1]), np.array([-0.5, -0.5, -0.5, 1]), np.array([0.5, -0.5, -0.5, 1])),

        # # top
        Triangle(np.array([-0.5, 0.5, -0.5, 1]), np.array([-0.5, 0.5, 0.5, 1]), np.array([0.5, 0.5, 0.5, 1])),
        Triangle(np.array([-0.5, 0.5, -0.5, 1]), np.array([0.5, 0.5, 0.5, 1]), np.array([0.5, 0.5, -0.5, 1])),

        # left
        Triangle(np.array([-0.5, 0.5, 0.5, 1]), np.array([-0.5, 0.5, -0.5, 1]), np.array([-0.5, -0.5, -0.5, 1])),
        Triangle(np.array([-0.5, 0.5, 0.5, 1]), np.array([-0.5, -0.5, -0.5, 1]), np.array([-0.5, -0.5, 0.5, 1])),

        # right
        Triangle(np.array([0.5, -0.5, -0.5, 1]), np.array([0.5, 0.5, -0.5, 1]), np.array([0.5, 0.5, 0.5, 1])),
        Triangle(np.array([0.5, -0.5, -0.5, 1]), np.array([0.5, 0.5, 0.5, 1]), np.array([0.5, -0.5, 0.5, 1])),

        # behind
        Triangle(np.array([0.5, -0.5, 0.5, 1]), np.array([-0.5, 0.5, 0.5, 1]), np.array([-0.5, -0.5, 0.5, 1])),
        Triangle(np.array([0.5, -0.5, 0.5, 1]), np.array([0.5, 0.5, 0.5, 1]), np.array([-0.5, 0.5, 0.5, 1])),
    ]

    return Object3d(mesh, np.array([-0.5, -0.5, 3, 0]))


def read_from_file(file_name: str) -> Object3d:
    start = timer()
    verts = []
    faces = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            if line.startswith("v"):
                ver = [float(i) for i in line[2:].split()]
                ver.append(1)
                verts.append(np.array(ver))
            if line.startswith("f"):
                vs = [int(i) for i in line[2:].split()]
                a = verts[vs[0] - 1]
                b = verts[vs[1] - 1]
                c = verts[vs[2] - 1]
                faces.append(Triangle(a, b, c))

    end = timer()
    print(f"file {file_name} was loaded: {end-start}")
    return Object3d(faces, np.array([0, 2.5, 8, 0]))




