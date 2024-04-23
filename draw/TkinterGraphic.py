from draw.AbstractGraphic import AbstractGraphic
from tkinter import Tk, Canvas
from timeit import default_timer as timer
from time import sleep


class TkinterGraphic(AbstractGraphic):

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()

    def clean(self):
        self.canvas.delete("all")

    def get_color(self, dot_prod: float) -> str:
        val = max(int(dot_prod * 230), 0)
        return '#{:02x}{:02x}{:02x}'.format(val, val, val)

    def draw_triangle(self, point1, point2, point3, color):
        self.canvas.create_polygon(
            point1[0], point1[1],
            point2[0], point2[1],
            point3[0], point3[1],
            fill=color
        )

    def update(self):
        self.window.update()

    def main_loop(self, tic_fun, max_fps: int):
        last_frame = 0
        frame_time = 1 / max_fps
        while True:
            start = timer()

            if start - last_frame > frame_time:
                last_frame = start
                tic_fun()

            self.window.update_idletasks()
            self.window.update()

            end = timer()
            # print(f"frame was generated: {end - start} \t {1 / (end - start)}FPS")
