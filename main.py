from numpy import array

from Camera import Camera
import Object3d
from draw.TkinterGraphic import TkinterGraphic


if __name__ == '__main__':
    width = 800
    height = 800

    graphic = TkinterGraphic(width, height)

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
        camera.setRotationMatrix(angleX, angleY, angleZ)
        camera.show(objs)
        angleX += -5
        # angleY += 20
        angleZ += -1

    graphic.main_loop(one_tic)
