from draw.AbstractGraphic import AbstractGraphic

import pygame
from timeit import default_timer as timer


class PygameGraphic(AbstractGraphic):

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.init = pygame.init()
        self.display_surface = pygame.display.set_mode((height, width))
        self.key_callback = None

    def clean(self):
        self.display_surface.fill((255, 255, 255))

    def draw_triangle(self, point1, point2, point3, color):
        pygame.draw.polygon(self.display_surface, color, (point1[:2], point2[:2], point3[:2]))
        pass

    def get_color(self, dot_prod: float) -> any:
        val = max(int(dot_prod * 230), 0)
        return val, val, val

    def update(self):
        pygame.display.update()

    def set_key_callback(self, f):
        self.key_callback = f

    def map_key(self, pygame_key) -> str:
        if pygame_key.key == pygame.K_UP:
            return "UP"
        if pygame_key.key == pygame.K_DOWN:
            return "DOWN"
        if pygame_key.key == pygame.K_LEFT:
            return "LEFT"
        if pygame_key.key == pygame.K_RIGHT:
            return "RIGHT"
        return pygame_key.unicode

    def main_loop(self, tic_fun, max_fps: int):
        last_frame = 0
        frame_time = 1 / max_fps
        while True:
            start = timer()
            if start - last_frame > frame_time:
                last_frame = start
                tic_fun()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # quit the program.
                    quit()
                    # Draws the surface object to the screen.
                if event.type == pygame.KEYDOWN:
                    if self.key_callback:
                        self.key_callback(self.map_key(event))

                pygame.display.update()

            end = timer()
            # print(f"frame was generated: {end - start} \t {1 / (end - start)}FPS")
