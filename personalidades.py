from serpiente import Serpiente

class SerpienteAgresiva(Serpiente):
    def __init__(self, x, y, color=..., velocidad=2, tamaño_segmento=10):
        super().__init__(x, y, color, velocidad, tamaño_segmento)

        self.objetivo_actual = None
        self.rango_agresion = 300

    def obtenerObjetivo(self, lista_serpientes):

        serpiente_cercana = None

        menor_distancia = float("inf") # distancia infinita

        for s in lista_serpientes:
            if s is self:
                continue

            distancia = self.pos.distance_to(s.pos)
            if distancia < menor_distancia and distancia < self.rango_agresion:
                menor_distancia = distancia
                serpiente_cercana = s

        self.objetivo_actual = serpiente_cercana


    def actualizar(self, dt):

        if self.sprint: self.velocidad = 3
        else: self.velocidad = 2

        movimiento = self.direccion * self.velocidad
        self.pos += movimiento

        self.distancia_acumulada += movimiento.length()

        while self.distancia_acumulada >= self.tamaño_segmento:
            self.segmentos.insert(0, self.pos.copy())
            self.distancia_acumulada -= self.tamaño_segmento

        while len(self.segmentos) > self.largo_objetivo:
            self.segmentos.pop()

        if self.sprint:
            self.tiempo_sprint += dt
            if self.tiempo_sprint >= 0.5:
                self.crecer(-1)
                self.tiempo_sprint = 0
        else:
            self.tiempo_sprint = 0

        self.obtenerObjetivo()
        while self.pos.y < self.objetivo_actual.pos.y:
            self.direccion = 