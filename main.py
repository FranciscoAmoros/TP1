import pygame

from puntos import Punto

# ------- VARIABLES --------

ancho_mundo = 5000
alto_mundo = 5000

# ------- VARIABLES DE JUEGO --------

puntos = []

CANTIDAD_INCIAL = 1500

running = True


pygame.init()

clock = pygame.time.Clock()


bg_image = pygame.image.load("imagenes/fondo.png")


def dibujarFondo(pantalla, ancho_pantalla, alto_pantalla):

    bg = pygame.transform.scale(bg_image, (ancho_pantalla, alto_pantalla))
    pantalla.blit(bg, (0,0))

def dibujarPuntosNuevos(pantalla):
    for p in puntos:
        p.draw(pantalla)

def ready(pantalla, ancho_pantalla, alto_pantalla):

    for i in range(CANTIDAD_INCIAL):
        puntos.append(Punto(ancho_mundo, alto_mundo))


    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dibujarFondo(pantalla, ancho_pantalla, alto_pantalla)
        dibujarPuntosNuevos(pantalla)


        # RENDER YOUR GAME HERE


        pygame.display.flip()

        clock.tick(60)

    pygame.quit()