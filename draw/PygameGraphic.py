from draw.AbstractGraphic import AbstractGraphic

import pygame
from timeit import default_timer as timer
from time import sleep


class PygameGraphic(AbstractGraphic):

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.init = pygame.init()
        self.display_surface = pygame.display.set_mode((height, width))

    def clean(self):
        self.display_surface.fill((255, 255, 255))

    def draw_triangle(self, point1, point2, point3, color):
        pygame.draw.polygon(self.display_surface, color, (point1[:2], point2[:2], point3[:2]))
        pass

    def get_color(self, norm, light) -> any:
        val = max(int(light.dot(norm) * 230), 0)
        return val, val, val

    def update(self):
        pygame.display.update()

    def main_loop(self, tic_fun):
        while True:
            start = timer()

            tic_fun()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # quit the program.
                    quit()
                    # Draws the surface object to the screen.
                pygame.display.update()

            end = timer()
            print(f"frame was generated: {end - start} \t {1 / (end - start)}FPS")
            sleep(1 / 30)
