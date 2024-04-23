import time
import numpy as np
from math import tan, radians

from Object3d import Object3d
from draw.AbstractGraphic import AbstractGraphic
from MyMath import normalize, normal, create_rotate_x, create_rotate_y, create_rotate_z


def quick_inverse(look_at_m: np.ndarray) -> np.ndarray:
    matrix = [
        [look_at_m[0][0], look_at_m[1][0], look_at_m[2][0], 0],
        [look_at_m[0][1], look_at_m[1][1], look_at_m[2][1], 0],
        [look_at_m[0][2], look_at_m[1][2], look_at_m[2][2], 0]
    ]

    return np.array([
        [look_at_m[0][0], look_at_m[1][0], look_at_m[2][0], 0],
        [look_at_m[0][1], look_at_m[1][1], look_at_m[2][1], 0],
        [look_at_m[0][2], look_at_m[1][2], look_at_m[2][2], 0],
        [-(look_at_m[3][0] * matrix[0][0] + look_at_m[3][1] * matrix[1][0] + look_at_m[3][2] * matrix[2][0]),
         -(look_at_m[3][0] * matrix[0][1] + look_at_m[3][1] * matrix[1][1] + look_at_m[3][2] * matrix[2][1]),
         -(look_at_m[3][0] * matrix[0][2] + look_at_m[3][1] * matrix[1][2] + look_at_m[3][2] * matrix[2][2]),
         1
         ]
    ])


def vector_cross_product(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    return np.array([
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
        1
        ])


def create_point_at(new_forward: np.ndarray, new_up: np.ndarray, new_right: np.ndarray, pos: np.ndarray):
    res = [
        [  new_right[0],   new_right[1],   new_right[2], 0],
        [     new_up[0],      new_up[1],      new_up[2], 0],
        [new_forward[0], new_forward[1], new_forward[2], 0],
        [        pos[0],         pos[1],         pos[2], 1]
    ]
    return np.array(res)


def point_at(pos: np.ndarray, target: np.ndarray, up: np.ndarray):
    """ Create pont at Matrix """
    new_forward = target - pos
    new_forward = normalize(new_forward)

    a = new_forward * (up @ new_forward)
    new_up = up - a
    new_up = normalize(new_up)
    new_right = vector_cross_product(new_up, new_forward)
    np.append(new_right, 1)

    return create_point_at(new_forward, new_up, new_right, pos)


class Camera:
    """ Object for rendering objects3d """
    def __init__(self, graphic: AbstractGraphic, theta: float = 45, z_near: float = 0.1, z_far: float = 1000):
        self.R = None
        self.rx_m = None
        self.ry_m = None
        self.rz_m = None
        self.yaw = 0
        self.graphic = graphic
        self.rotX = 0
        self.rotZ = 0
        self.light = normalize(np.array([-1, -1, -1], dtype=np.float64))
        self.position = np.array([0, 0, 0, 1], dtype=np.float64)
        a = self.graphic.width / self.graphic.height
        f = 1 / tan((radians(theta) * 0.5))
        q = z_far / (z_far - z_near)

        self.P = np.array([
            [a * f, 0,            0, 0],
            [0,     f,            0, 0],
            [0,     0,            q, 1],
            [0,     0, (- z_far * z_near) / (z_far - z_near), 0],
        ])
        self.set_rotation_matrix(0, 0, 0)

    def set_rotation_matrix(self, rot_x: float, rot_y: float, rot_z: float):
        rad_x = radians(rot_x)
        rad_y = radians(rot_y)
        rad_z = radians(rot_z)
        self.rx_m = create_rotate_x(rad_x)
        self.ry_m = create_rotate_y(rad_y)
        self.rz_m = create_rotate_z(rad_z)
        self.R = self.rx_m @ self.ry_m @ self.rz_m

    def position_rest(self):
        self.position = np.array([0, 0, 0, 1], dtype=np.float64)

    def move_camera_by(self, to_add: np.ndarray) -> None:
        """ Move position of camera in 3d space by vector"""
        target = to_add
        camera_rot_m = create_rotate_y(self.yaw)
        look_dir = target @ camera_rot_m
        self.position += to_add
        self.position[3] = 1

    def project(self, v: np.ndarray):
        """ Old projection function, one vertex at the time """
        new_v = v @ self.P
        if new_v[3] != 0:
            new_v /= new_v[3]
        return new_v

    def project2(self, v: np.ndarray, scale_w, scale_h):
        """ Matrix projection function, all at once """
        new_v = v @ self.P
        w3 = new_v[:, 3]
        new_v[:, 0] /= w3
        new_v[:, 1] /= w3
        new_v[:, 2] /= w3

        new_v += 1
        new_v[:, 0] *= scale_w
        new_v[:, 1] *= scale_h

        new_v[:, 3] = 1
        return new_v

    def show(self, objects: list[Object3d]):
        """ Render given objects """

        to_draw = []
        scale_w = 0.5 * self.graphic.width
        scale_h = 0.5 * self.graphic.height

        up = np.array([0, 1, 0, 1])
        target = np.array([0, 0, 1, 1])
        camera_rot_m = create_rotate_y(self.yaw)
        look_dir = target @ camera_rot_m
        target = self.position + look_dir
        target[3] = 1
        up[3] = 1
        camera_m = point_at(self.position, target, up)
        view_m = quick_inverse(camera_m)

        # Filter triangles
        start = time.time()
        self.graphic.clean()
        for obj in objects:
            start_r = time.time()
            mesh_rotated_m = obj.vs_m
            mesh_rotated_m = obj.vs_m @ self.R
            mesh_rotated_m += obj.pos
            mesh_rotated_m = mesh_rotated_m @ view_m

            normals_m = obj.normal_m
            normals_m = obj.normal_m @ self.R
            # normals_m = normals_m @ view_m
            normals_m = normals_m[:, 0:3]
            color_normals = normals_m @ self.light

            mesh_projected_m = self.project2(mesh_rotated_m, scale_w, scale_h)

            end_r = time.time()
            # print(f"Prepare data NP in: {end_r - start_r}")

            start_filter = time.time()
            for i in range(0, len(obj.triangles)):
                tria = obj.triangles[i]
                v1 = mesh_rotated_m[tria[0]]

                norm = normals_m[i]

                if (v1[:3] - self.position[:3]).dot(norm) < 0:

                    d1 = mesh_rotated_m[tria[0]][2] - self.position[2]
                    d2 = mesh_rotated_m[tria[1]][2] - self.position[2]
                    d3 = mesh_rotated_m[tria[2]][2] - self.position[2]

                    v1 = mesh_projected_m[tria[0]]
                    v2 = mesh_projected_m[tria[1]]
                    v3 = mesh_projected_m[tria[2]]

                    c = color_normals[i]
                    cl = self.graphic.get_color(float(c))
                    to_draw.append(((d1 + d2 + d3) / 3, v1, v2, v3, cl))
            end_filter = time.time()
            # print(f"Filter vert in: {end_filter - start_filter}")

        end = time.time()
        # print(f"Projected in {end-start}")

        start_draw = time.time()
        to_draw.sort(key=lambda a: a[0], reverse=True)
        # Start rendering
        for mid, v1, v2, v3, cl in to_draw:
            self.graphic.draw_triangle(v1, v2, v3, cl)

        end_draw = time.time()
        # print(f"Cycle in {end_draw - start_draw}")

        self.graphic.update()


