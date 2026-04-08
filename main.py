import pygame

from puntos import Punto

from boton import Boton

# ------- VARIABLES --------

ancho_pantalla = 800
alto_pantalla = 600

ancho_mundo = 5000
alto_mundo = 5000

# ------- VARIABLES DE JUEGO --------

puntos = []

CANTIDAD_INCIAL = 1500

running = True


pygame.init()
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
clock = pygame.time.Clock()


bg_image = pygame.image.load("imagenes/fondo.png")

for i in range(CANTIDAD_INCIAL):
    puntos.append(Punto(ancho_mundo, alto_mundo))


def dibujarFondo():

    bg = pygame.transform.scale(bg_image, (ancho_pantalla, alto_pantalla))
    screen.blit(bg, (0,0))

def dibujarPuntosNuevos():
    for p in puntos:
        p.draw(screen)

# ---- MENU -------

botones = []

boton_jugar = Boton("imagenes/boton_jugar.png", 0, 0)

botones.append(boton_jugar)


boton_jugar.rect.centerx = ancho_pantalla // 2
boton_jugar.rect.centery = alto_pantalla // 2 + alto_pantalla // 4


def dibujarMenu(pantalla):
    boton_jugar.dibujar(pantalla)



while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in botones:
                if b.clickeado(event.pos):
                    print("Se clickeó:")

    dibujarFondo()
    dibujarMenu(screen)
    #dibujarPuntosNuevos()


    # RENDER YOUR GAME HERE


    pygame.display.flip()

    clock.tick(60)

pygame.quit()