import numpy as np
import tkinter as tk
from timeit import default_timer as timer
from math import tan, sin, cos, radians

from draw import draw_triangle

from Object3d import Object3d


class Camera:
    def __init__(self, canvas: tk.Canvas, width: int, height: int, theta: float = 90, z_near: float = 0.1, z_far: float = 1000):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.rotX = 0
        self.rotZ = 0
        self.light = np.array([0, 0, -1])
        self.light = self.light / np.linalg.norm(self.light)
        self.position = np.array([0, 0, 0])
        a = width / height
        f = 1 / tan((radians(theta) * 0.5))
        q = z_far / (z_far - z_near)

        self.P = np.array([
            [a * f, 0,            0, 0],
            [0,     f,            0, 0],
            [0,     0,            q, 1],
            [0,     0, (- z_far * z_near) / (z_far - z_near), 0],
        ])
        self.RX = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.RZ = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.RY = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.R = self.RX @ self.RY @ self.RZ

    def setRotationMatrix(self, rotX, rotY, rotZ):

        angX = radians(rotX) * 0.5
        angZ = radians(rotZ)

        self.RX = np.array([
            [1, 0, 0, 0],
            [0, cos(angX), sin(angX), 0],
            [0, -sin(angX), cos(angX), 0],
            [0, 0, 0, 1]
        ])

        self.RZ = np.array([
            [cos(angZ), sin(angZ), 0, 0],
            [-sin(angZ), cos(angZ), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.R = self.RX @ self.RY @ self.RZ

    def clean(self) -> None:
        self.canvas.delete("all")

    def project(self, v: np.ndarray):
        new_v = v @ self.P
        if new_v[3] != 0:
            new_v /= new_v[3]
        return new_v

    def get_color(self, norm) -> str:
        val = max(int(self.light.dot(norm) * 230), 0)
        return '#{:02x}{:02x}{:02x}'.format(val, val, val)

    def show(self, objects: list[Object3d]):
        to_draw = []
        scale_w = 0.5 * self.width
        scale_h = 0.5 * self.height
        for obj in objects:
            for tria in obj.mesh:
                vs = tria.vs
                vs = vs @ self.R
                vs += obj.pos

                v1 = vs[0]
                v2 = vs[1]
                v3 = vs[2]
                norm = tria.normal @ self.R
                norm = norm[:3]

                if (v1[:3] - self.position).dot(norm) < 0:
                    v1 = self.project(v1)
                    v1 += 1
                    v1[0] *= scale_w
                    v1[1] *= scale_h

                    v2 = self.project(v2)
                    v2 += 1
                    v2[0] *= scale_w
                    v2[1] *= scale_h

                    v3 = self.project(v3)
                    v3 += 1
                    v3[0] *= scale_w
                    v3[1] *= scale_h

                    cl = self.get_color(norm)
                    to_draw.append((v1, v2, v3, cl))

        to_draw = sorted(to_draw, key=lambda a: (a[0][2] + a[1][2] + a[2][2]) / 3, reverse=True)
        for v1, v2, v3, cl in to_draw:
            draw_triangle(self.canvas, v1, v2, v3, cl)

