import pygame
import math

class Serpiente:
    def __init__(self, x, y, color=(0,255,0), velocidad=2, tamaño_segmento=10):
        self.pos = pygame.Vector2(x, y)
        self.direccion = pygame.Vector2(1, 0)
        self.velocidad = velocidad
        self.tamaño_segmento = tamaño_segmento
        
        self.segmentos = [self.pos.copy()]
        self.largo_objetivo = 40

        self.color = color

    def actualizar(self):
  
        self.pos += self.direccion * self.velocidad

        self.segmentos.insert(0, self.pos.copy())

        if len(self.segmentos) > self.largo_objetivo:
            self.segmentos.pop()


    def crecer(self, cantidad=2):
        self.largo_objetivo += cantidad

    def dibujar(self, pantalla, cam_x, cam_y):
        for s in self.segmentos:
            pygame.draw.circle(
                pantalla, 
                self.color,
                (int(s.x - cam_x), int(s.y - cam_y)),
                self.tamaño_segmento
            )

    def get_head_hitbox(self): # funcion que devuelve la collision solo de la cabeza

        return (self.pos.x, self.pos.y, self.tamaño_segmento)

    def get_body_hitboxes(self): # funcion que devuelve la collision solo del cuerpo

        hitboxes = []
        for s in self.segmentos[1:]:
            hitboxes.append((s.x, s.y, self.tamaño_segmento))
        return hitboxes
    
    def set_direccion_con_mouse(self):

            mx, my = pygame.mouse.get_pos()
            dir_vec = pygame.Vector2(mx, my) - pygame.Vector2(400, 300)
            if dir_vec.length() > 0:
                self.direccion = dir_vec.normalize()