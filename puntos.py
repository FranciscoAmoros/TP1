import random
import pygame

class Punto:
    def __init__(self, ancho, alto, posicion=None):

        if isinstance(posicion, pygame.Vector2):
            self.x, self.y = posicion
        else:

            self.x = random.randint(0, ancho)
            self.y = random.randint(0, alto)
            
        self.size = random.randint(2, 7)
        self.color = (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255)
        )

    def draw(self, pantalla, cam_x, cam_y):
        pygame.draw.circle(pantalla, self.color, (self.x - cam_x, self.y - cam_y), self.size)