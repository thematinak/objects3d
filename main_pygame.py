import numpy as np
from numpy import array

from Camera import Camera
import Object3d
from draw.PygameGraphic import PygameGraphic


if __name__ == '__main__':
    width = 800
    height = 800

    graphic = PygameGraphic(width, height)

    camera: Camera = Camera(graphic, width, height)

    cube1 = Object3d.make_cube()
    cube2 = Object3d.make_cube()
    cube2.pos = array([5, 5, 20, 0])
    objs = [
        # Object3d.read_from_file("recikolin_smal_ficker.obj")
        # Object3d.read_from_file("untitled.obj")
        # cube1, cube2
        cube1
    ]

    angleX = 0
    angleY = 0
    angleZ = 0

    def one_tic():
        global angleX, angleY, angleZ
        camera.set_rotation_matrix(angleX, angleY, angleZ)
        camera.show(objs)
        angleX += 1
        angleY += 2
        # angleZ += -1

    def on_key(key):
        if "r" == key:
            camera.position_rest()
        if "p" == key:
            print(f"({angleX}, {angleY}, {angleZ}, {camera.yaw})")
        if "LEFT" == key:
            camera.move_camera_by(np.array([-1, 0, 0, 0], dtype=np.float64))
            return
        if "RIGHT" == key:
            camera.move_camera_by(np.array([1, 0, 0, 0], dtype=np.float64))
            return
        if "UP" == key:
            camera.move_camera_by(np.array([0, -1, 0, 0], dtype=np.float64))
            return
        if "DOWN" == key:
            camera.move_camera_by(np.array([0, 1, 0, 0], dtype=np.float64))
            return

        if "w" == key:
            camera.move_camera_by(np.array([0, 0, 1, 0], dtype=np.float64))
            return
        if "s" == key:
            camera.move_camera_by(np.array([0, 0, -1, 0], dtype=np.float64))
            return
        if "a" == key:
            camera.yaw += .1
            return
        if "d" == key:
            camera.yaw -= .1
            return
        pass

    graphic.set_key_callback(on_key)

    graphic.main_loop(one_tic, 60)
