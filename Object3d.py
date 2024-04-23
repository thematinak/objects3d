import numpy as np
from timeit import default_timer as timer


def normalize(v: np.ndarray):
    return v / np.linalg.norm(v)


def normal(t1: np.ndarray, t2: np.ndarray, t3: np.ndarray):
    v1 = t2 - t1
    v2 = t3 - t1
    res = normalize(np.cross(v1[0:3], v2[0:3]))
    return np.append(res, 1)


class Object3d:
    def __init__(self, vs: np.ndarray, triangles: list[(int, int, int)], pos: np.ndarray, scale: np.ndarray = np.array([1, 1, 1, 1])):
        self.pos = pos
        self.scale = scale

        self.vs_m = vs
        self.triangles: list[(int, int, int)] = triangles
        normal_m = []
        for t1, t2, t3 in triangles:
            normal_m.append(normal(self.vs_m[t1], self.vs_m[t2], self.vs_m[t3]))
        self.normal_m = np.array(normal_m)


def make_cube() -> Object3d:
    vs = np.array([
        [-0.5, -0.5, -0.5, 1],
        [-0.5, 0.5, -0.5, 1],
        [0.5, 0.5, -0.5, 1],
        [0.5, -0.5, -0.5, 1],
        [0.5, -0.5, 0.5, 1],
        [-0.5, -0.5, 0.5, 1],
        [-0.5, 0.5, 0.5, 1],
        [0.5, 0.5, 0.5, 1]
    ])

    triangles = [
        (0, 1, 2),
        (0, 2, 3),

        (4, 5, 0),
        (4, 0, 3),

        (1, 6, 7),
        (1, 7, 2),

        (6, 1, 0),
        (6, 0, 5),

        (3, 2, 7),
        (3, 7, 4),

        (4, 6, 5),
        (4, 7, 6),
    ]

    return Object3d(vs, triangles, np.array([-0.5, -0.5, 3, 0]))


def read_from_file(file_name: str) -> Object3d:
    start = timer()
    verts = []
    faces: (int, int, int) = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            if line.startswith("v"):
                ver = [float(i) for i in line[2:].split()]
                ver.append(1)
                verts.append(np.array(ver))
            if line.startswith("f"):
                vs = [int(i) for i in line[2:].split()]
                a = vs[0] - 1
                b = vs[1] - 1
                c = vs[2] - 1
                faces.append((a, b, c))
    verts = np.array(verts)
    end = timer()
    print(f"file {file_name} was loaded: {end-start}")
    return Object3d(verts, faces, np.array([0, 2.5, 8, 0]))
