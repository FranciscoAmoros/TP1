import pygame

from puntos import Punto

from boton import Boton

from serpiente import Serpiente

import random


# ------- VARIABLES --------

ancho_pantalla = 800
alto_pantalla = 600

ancho_mundo = 5000
alto_mundo = 5000

# ------- VARIABLES DE JUEGO --------

modo_juego = "local"


jugador : Serpiente
sprint = False

bots = []

puntos = []

CANTIDAD_JUGADORES_MIN = 6

CANTIDAD_INCIAL = 1500

running = True

running_menu = True


pygame.init()
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
clock = pygame.time.Clock()


bg_image = pygame.image.load("imagenes/fondo_juego.png")

for i in range(CANTIDAD_INCIAL):
    puntos.append(Punto(ancho_mundo, alto_mundo))


def dibujarFondo(cam_x, cam_y):

    global bg_image


    
    bg_w, bg_h = bg_image.get_size()
    bg_w, bg_h = bg_w*4, bg_h*4

    bg = pygame.transform.scale(bg_image, (bg_w, bg_h))


    

    start_x = -cam_x % bg_w
    start_y = -cam_y % bg_h

    for x in range(-bg_w, ancho_pantalla + bg_w, bg_w):
        for y in range(-bg_h, alto_pantalla + bg_h, bg_h):
            screen.blit(bg, (start_x + x, start_y + y))

def dibujarPuntosNuevos(cam_x, cam_y):
    for p in puntos:
        p.draw(screen, cam_x, cam_y)

# ---- MENU -------

botones = []

boton_jugar = Boton("imagenes/boton base.jpg", 0, 0, "local", 0.2)
boton_ajustes = Boton("imagenes/boton base.jpg", 0, 0, "red", 0.2)
boton_salir = Boton("imagenes/boton base.jpg", 0, 0, "salir", 0.2)

botones.append(boton_jugar)
botones.append(boton_ajustes)
botones.append(boton_salir)


boton_jugar.rect.centerx = ancho_pantalla // 2
boton_jugar.rect.centery = alto_pantalla // 2 + alto_pantalla // 8

boton_ajustes.rect.centerx = ancho_pantalla // 2
boton_ajustes.rect.centery = alto_pantalla // 2 + alto_pantalla // 4 + 20

boton_salir.rect.centerx = ancho_pantalla // 2
boton_salir.rect.centery = alto_pantalla // 2 + alto_pantalla // 4 + alto_pantalla // 8 + 40


def dibujarMenu():
    bg = pygame.transform.scale(bg_image, (ancho_pantalla, alto_pantalla))
    screen.blit(bg, (0,0))
    boton_jugar.dibujar(screen)
    boton_ajustes.dibujar(screen)
    boton_salir.dibujar(screen)

def onClicked(boton="salir"):

    global running, running_menu, modo_juego

    if boton == "salir":
        running = False
    if boton == "local":
        running_menu = False
        modo_juego = "local"
        startLocalGame()

    if boton == "red":
        modo_juego = "multijugador"
        pass
    
def startLocalGame():

    global jugador, bots
    
    jugador = Serpiente(300, 200)


    for i in range(CANTIDAD_JUGADORES_MIN - 1):

        pos_valida = False

        while not pos_valida:
            pos_bot_x, pos_bot_y = random.randint(50, ancho_mundo - 50), random.randint(50, alto_mundo - 50)

            # aca revisar que no haya un bot o jugador DEMASIADO cerca


        bot = Serpiente()
        bots.append(bot)


def colisiones_circulos(x1, y1, r1, x2, y2, r2): # funcion que detecta las collisiones entre cirulos

    return (x1 - x2)**2 + (y1 - y2)**2 <= (r1 + r2)**2 # midiendo la distancia y el radio



while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if running_menu:
                for b in botones:
                    if b.clickeado(event.pos):
                        print("Se clickeó: ", b.nombre)
                        onClicked(b.nombre)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                if not running_menu:
                    sprint = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                if not running_menu:
                    sprint = False

    

    if running_menu: # si esta en el menu hace unicamente lo del menu

        dibujarMenu()

        pygame.display.flip()
        clock.tick(60)
        continue


    if isinstance(jugador, Serpiente):


        cam_x = jugador.pos.x - ancho_pantalla // 2
        cam_y = jugador.pos.y - alto_pantalla // 2

        if sprint:
            jugador.velocidad = 3
            #jugador.crecer(-2)
        else:
            jugador.velocidad = 2

        dibujarFondo(cam_x, cam_y)

        jugador_head_collision = jugador.get_head_hitbox()
        jugador_body_collision = jugador.get_body_hitboxes()


        hitbox_x, hitbox_y, hitbox_radius = jugador_head_collision # variables para la cabeza del jugador

        for p in puntos[:]:
            if colisiones_circulos(hitbox_x, hitbox_y, hitbox_radius, p.x, p.y, p.size):
                jugador.crecer(p.size)
                puntos.remove(p)
        

        jugador.set_direccion_con_mouse()
        jugador.actualizar()

        dibujarPuntosNuevos(cam_x, cam_y) # dibujar primero los puntos antes que el jugador

        jugador.dibujar(screen, cam_x, cam_y)




    # RENDER YOUR GAME HERE


    pygame.display.flip()

    clock.tick(60)

pygame.quit()