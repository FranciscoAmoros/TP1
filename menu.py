import pygame

ancho_pantalla = 800
alto_pantalla = 600


bg_image = pygame.image.load("imagenes/fondo.png")

running = True

pygame.init()

pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))

bg = pygame.transform.scale(bg_image, (ancho_pantalla, alto_pantalla))
pantalla.blit(bg, (0,0))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # RENDER YOUR GAME HERE


    pygame.display.flip()


