import tkinter
from time import sleep
from timeit import default_timer as timer

from numpy import array

from Camera import Camera
import Object3d

if __name__ == '__main__':
    width = 800
    height = 800

    window = tkinter.Tk()

    canvas = tkinter.Canvas(window, width=width, height=height)
    canvas.update()
    canvas.pack()

    camera: Camera = Camera(canvas, width, height)

    cube1 = Object3d.make_cube()
    cube2 = Object3d.make_cube()
    cube2.pos = array([5, 5, 20, 0])
    objs = [
        Object3d.read_from_file("recikolin_smal_ficker.obj")
        # Object3d.read_from_file("untitled.obj")
        # cube1, cube2
        # cube1
    ]

    angleX = 0
    angleY = 0
    angleZ = 0
    for i in range(0, 10000):
        start = timer()
        camera.setRotationMatrix(angleX, angleY, angleZ)
        camera.clean()
        camera.show(objs)
        angleX += -5
        # angleY += 20
        angleZ += -1
        window.update()
        end = timer()
        print(f"frame {i} was generated: {end-start} \t {1/(end-start)}FPS")
        sleep(1/60)

    tkinter.mainloop()
