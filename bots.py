from serpiente import Serpiente

import pygame

import random

class SerpienteAgresiva(Serpiente):
    def __init__(self, x, y, color=..., velocidad=2, tamaño_segmento=10):
        super().__init__(x, y, color, velocidad, tamaño_segmento)

        self.objetivo_actual = None
        self.rango_agresion = 300

        self.perseguir_puntos = False
        self.movimiento_random = True
        self.is_direction_set = False

        self.contador_switcher = 0
        self.tiempo_switch = 5
        

    def obtenerObjetivo(self, lista_serpientes):

        serpiente_cercana = None

        menor_distancia = float("inf") # distancia infinita

        for s in lista_serpientes:
            if s is self or isinstance(s, SerpienteAgresiva):
                continue

            distancia = self.pos.distance_to(s.pos)
            if distancia < menor_distancia and distancia < self.rango_agresion:
                menor_distancia = distancia
                serpiente_cercana = s

        self.objetivo_actual = serpiente_cercana


    def actualizar(self, dt, serpientes, puntos, jugador):

        if self.sprint: self.velocidad = 180
        else: self.velocidad = 120

        movimiento = self.direccion * self.velocidad * dt
        self.pos += movimiento

        self.distancia_acumulada += movimiento.length()

        while self.distancia_acumulada >= self.tamaño_segmento:
            self.segmentos.insert(0, self.pos.copy())
            self.distancia_acumulada -= self.tamaño_segmento

        while len(self.segmentos) > self.largo_objetivo and len(self.segmentos) > 1:
            self.segmentos.pop()

        if self.sprint:
            self.tiempo_sprint += dt
            if self.tiempo_sprint >= 0.5:
                self.crecer(-1)
                self.tiempo_sprint = 0
        else:
            self.tiempo_sprint = 0

        self.contador_switcher += dt

        self.obtenerObjetivo(serpientes)

        if self.objetivo_actual is not None:

            self.sprint = True

            anticipacion = 80
            punto_futuro = self.objetivo_actual.pos + self.objetivo_actual.direccion * anticipacion

            direccion_obj = punto_futuro - self.pos
            if direccion_obj.length() > 0:
                direccion_obj = direccion_obj.normalize()

            dx = self.objetivo_actual.direccion.x
            dy = self.objetivo_actual.direccion.y

            perp1 = pygame.Vector2(-dy, dx)
            perp2 = pygame.Vector2(dy, -dx)

            vec_obj = self.objetivo_actual.pos - self.pos
            direccion_lateral = perp1 if vec_obj.dot(perp1) > 0 else perp2

            distancia = vec_obj.length()
            if distancia < 75:
                direccion_obj = (direccion_obj + direccion_lateral * 0.5).normalize()

            else:

                punto_enfrente = self.pos + self.direccion * 120

                for segmento in self.objetivo_actual.segmentos:
                    if segmento.distance_to(punto_enfrente) < 60:

                        hacia_objetivo = vec_obj.normalize()

                        esquive = direccion_obj.rotate(30)

                        direccion_obj = (esquive * 0.6 + hacia_objetivo * 0.4).normalize()


            self.direccion = direccion_obj.normalize()

        else:
            self.sprint = False

            if self.contador_switcher > self.tiempo_switch:

                self.contador_switcher = 0
                self.tiempo_switch = random.randint(3, 7)

                self.perseguir_puntos = not self.perseguir_puntos
                self.movimiento_random = not self.movimiento_random

                self.is_direction_set = False

            if self.movimiento_random and not self.is_direction_set:
                self.set_random_direction()
                self.is_direction_set = True

            if self.perseguir_puntos:


                punto_mas_cercano = None
                menor_dist = float("inf")

                for p in puntos:
                    dist = self.pos.distance_to(p.pos)

                    if dist < menor_dist:
                        menor_dist = dist
                        punto_mas_cercano = p

                if punto_mas_cercano is not None:


                    direccion = (punto_mas_cercano.pos - self.pos)
                    if direccion.length() != 0:
                        ruido = random.uniform(-80, 80)
                        direccion = direccion.rotate(ruido)
                        direccion = direccion.normalize()
                        self.direccion = direccion

class SerpienteComePuntos(Serpiente):
    def __init__(self, x, y, color=..., velocidad=2, tamaño_segmento=10):
        super().__init__(x, y, color, velocidad, tamaño_segmento)

        self.perseguir_puntos = False
        self.movimiento_random = True
        self.is_direction_set = False

        self.contador_switcher = 0
        self.tiempo_switch = 5

    def actualizar(self, dt, serpientes, puntos, jugador):

        if self.sprint: self.velocidad = 180
        else: self.velocidad = 120

        movimiento = self.direccion * self.velocidad * dt
        self.pos += movimiento

        self.distancia_acumulada += movimiento.length()

        while self.distancia_acumulada >= self.tamaño_segmento:
            self.segmentos.insert(0, self.pos.copy())
            self.distancia_acumulada -= self.tamaño_segmento

        while len(self.segmentos) > self.largo_objetivo and len(self.segmentos) > 1:
            self.segmentos.pop()

        if self.sprint:
            self.tiempo_sprint += dt
            if self.tiempo_sprint >= 0.5:
                self.crecer(-1)
                self.tiempo_sprint = 0
        else:
            self.tiempo_sprint = 0
            
        self.contador_switcher += dt

        if self.contador_switcher > self.tiempo_switch:

            self.contador_switcher = 0


            self.perseguir_puntos = not self.perseguir_puntos
            self.movimiento_random = not self.movimiento_random

            if self.perseguir_puntos:
                self.tiempo_switch = random.randint(6, 10)
            else:
                self.tiempo_switch = random.randint(2, 4)

            self.is_direction_set = False

        if self.movimiento_random and not self.is_direction_set:

            self.sprint = False

            self.set_random_direction()
            self.is_direction_set = True

        if self.perseguir_puntos:

            self.sprint = True


            punto_mas_cercano = None
            menor_dist = float("inf")

            for p in puntos:
                dist = self.pos.distance_to(p.pos)

                if dist < menor_dist:
                    menor_dist = dist
                    punto_mas_cercano = p

            if punto_mas_cercano is not None:


                direccion = (punto_mas_cercano.pos - self.pos)
                if direccion.length() != 0:
                    ruido = random.uniform(-60, 60)
                    direccion = direccion.rotate(ruido)
                    direccion = direccion.normalize()
                    self.direccion = direccion

class SerpienteMiedosa(Serpiente):
    
    def __init__(self, x, y, color=..., velocidad=2, tamaño_segmento=10):
        super().__init__(x, y, color, velocidad, tamaño_segmento)
        
        self.perseguir_puntos = False
        self.movimiento_random = True
        self.is_direction_set = False

        self.contador_switcher = 0
        self.tiempo_switch = 5
        
        self.escape_time = 2
        
        self.escape_timer = 2
        
    def actualizar(self, dt, serpientes, puntos, jugador):

        if self.sprint: self.velocidad = 180
        else: self.velocidad = 120

        movimiento = self.direccion * self.velocidad * dt
        self.pos += movimiento

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
        
            
        self.contador_switcher += dt
        
        self.escape_timer += dt
        
        for segmento in jugador.segmentos:
            if self.pos.distance_to(segmento) < 100 and self.escape_timer >= self.escape_time:
                self.escapar(jugador)
                return
        

        if self.contador_switcher > self.tiempo_switch:

            self.contador_switcher = 0


            self.perseguir_puntos = not self.perseguir_puntos
            self.movimiento_random = not self.movimiento_random

            if self.perseguir_puntos:
                self.tiempo_switch = random.randint(3, 4)
            else:
                self.tiempo_switch = random.randint(5, 6)

            self.is_direction_set = False

        if self.movimiento_random and not self.is_direction_set:

            self.sprint = False

            self.set_random_direction()
            self.is_direction_set = True

        if self.perseguir_puntos:

            self.sprint = True


            punto_mas_cercano = None
            menor_dist = float("inf")

            for p in puntos:
                dist = self.pos.distance_to(p.pos)

                if dist < menor_dist:
                    menor_dist = dist
                    punto_mas_cercano = p

            if punto_mas_cercano is not None:


                direccion = (punto_mas_cercano.pos - self.pos)
                if direccion.length() != 0:
                    ruido = random.uniform(-120, 120)
                    direccion = direccion.rotate(ruido)
                    direccion = direccion.normalize()
                    self.direccion = direccion

    def escapar(self, jugador):
        
        dir = (self.pos - jugador.pos).normalize()
        
        self.direccion = dir
        
        self.escape_timer = 0.0
        
        self.sprint = True