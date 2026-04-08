import random
import pygame

class Punto:
    def __init__(self, ancho, alto):
        self.x = random.randint(0, ancho)
        self.y = random.randint(0, alto)
        self.size = random.randint(3, 6)
        self.color = (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255)
        )

    def draw(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.size)