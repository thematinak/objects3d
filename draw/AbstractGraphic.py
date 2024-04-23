

class AbstractGraphic:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def clean(self):
        pass

    def draw_triangle(self, point1, point2, point3, color):
        pass

    def get_color(self, dot_prod: float) -> any:
        pass

    def update(self):
        pass
