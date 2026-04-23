import pygame
import math
import random


class Serpiente:
    def __init__(self, x, y, nombre, centro_mundo, radio_mundo, color=(0,255,0), velocidad=2, tamaño_segmento=10):
        self.pos = pygame.Vector2(x, y)
        self.direccion = pygame.Vector2(1, 0)
        self.velocidad = velocidad
        self.tamaño_segmento = tamaño_segmento

        self.centro_mundo = centro_mundo
        self.radio_mundo = radio_mundo
        
        self.segmentos = [self.pos.copy()]
        self.largo_objetivo = 10
        self.distancia_acumulada = 0

        self.color = color
        self.nombre = nombre

        self.sprint = False
        self.tiempo_sprint = 0

        self.contador_puntos_consumidos = 0


    def actualizar(self, dt):

        if self.sprint: self.velocidad = 180
        else: self.velocidad = 120

        movimiento = self.direccion * self.velocidad * dt
        self.pos += movimiento

        dx = self.pos.x - self.centro_mundo[0]
        dy = self.pos.y - self.centro_mundo[1]

        dist_sq = dx*dx + dy*dy

        if dist_sq > self.radio_mundo * self.radio_mundo:
            dist = math.sqrt(dist_sq)
            factor = self.radio_mundo / dist
            self.pos.x = self.centro_mundo[0] + dx * factor
            self.pos.y = self.centro_mundo[1] + dy * factor

        self.distancia_acumulada += movimiento.length()

        while self.distancia_acumulada >= self.tamaño_segmento:
            self.segmentos.insert(0, self.pos.copy())
            self.distancia_acumulada -= self.tamaño_segmento

        while len(self.segmentos) > self.largo_objetivo and len(self.segmentos) > 5:
            self.segmentos.pop()

        if self.sprint:
            self.tiempo_sprint += dt
            if self.tiempo_sprint >= 0.5:
                self.crecer(-1)
                self.tiempo_sprint = 0
        else:
            self.tiempo_sprint = 0


    def crecer(self, cantidad):
        self.tamaño_segmento += cantidad / 30
        self.largo_objetivo += cantidad/4
        self.contador_puntos_consumidos += cantidad
        if self.largo_objetivo < 5:
            self.largo_objetivo = 5
            
        if self.contador_puntos_consumidos < 5:
            self.contador_puntos_consumidos = 5

    def dibujar(self, pantalla, cam_x=0, cam_y=0):
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

    def set_random_direction(self):

        dir = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.direccion = dir


