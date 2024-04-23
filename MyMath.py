import numpy as np
from math import sin, cos


def normalize(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def normal(t1: np.ndarray, t2: np.ndarray, t3: np.ndarray):
    v1 = t2 - t1
    v2 = t3 - t1
    res = normalize(np.cross(v1[0:3], v2[0:3]))
    return np.append(res, 1)


def create_rotate_x(angle: float) -> np.ndarray:
    return np.array([
            [1, 0, 0, 0],
            [0, cos(angle), sin(angle), 0],
            [0, -sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])


def create_rotate_y(angle: float) -> np.ndarray:
    return np.array([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])


def create_rotate_z(angle: float) -> np.ndarray:
    return np.array([
        [cos(angle), sin(angle), 0, 0],
        [-sin(angle), cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
