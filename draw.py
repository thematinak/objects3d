import tkinter as tk


def draw_triangle(canvas: tk.Canvas, point1, point2, point3, color):
    canvas.create_polygon(
        point1[0], point1[1],
        point2[0], point2[1],
        point3[0], point3[1],
        fill=color
    )
