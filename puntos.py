import random
import pygame
import math

class Punto:
    def __init__(self, radio, centro, posicion=None):

        if isinstance(posicion, pygame.Vector2):
            self.x, self.y = posicion
        else:

            angle = random.uniform(0, 2 * math.pi)
            r = radio * math.sqrt(random.random())

            self.x = centro[0] + r * math.cos(angle)
            self.y = centro[1] + r * math.sin(angle)
        
        self.pos = (self.x, self.y)
            
        self.size = random.randint(2, 7)
        self.color = (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255)
        )

    def draw(self, pantalla, cam_x, cam_y):
        pygame.draw.circle(pantalla, self.color, (self.x - cam_x, self.y - cam_y), self.size)