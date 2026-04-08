import pygame

class Boton:
    def __init__(self, ruta_imagen, x, y, escala=1):
        self.imagen_inicial = pygame.image.load(ruta_imagen).convert_alpha()
        
        if isinstance(escala, (int, float)): # verificacion de que el parametro escala sea int o float
            nuevo_ancho = int(self.imagen_inicial.get_width() * escala)
            nuevo_alto = int(self.imagen_inicial.get_height() * escala)

        else:

            nuevo_ancho, nuevo_alto = escala # si la escala no es un numero, espero un tamaño especifico (x, y)

        
        self.imagen = pygame.transform.smoothscale(self.imagen_inicial, (nuevo_ancho, nuevo_alto))
        self.rect = self.imagen.get_rect(topleft=(x, y))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def clickeado(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)