import pygame

from puntos import Punto

from boton import Boton

from serpiente import Serpiente

from bots import SerpienteAgresiva
from bots import SerpienteComePuntos
from bots import SerpienteMiedosa

import random

import math

import collisiones as col

import UI


clases_bots = [SerpienteAgresiva, SerpienteComePuntos, SerpienteMiedosa]



# ------- VARIABLES --------

ancho_pantalla = 800
alto_pantalla = 600

ancho_mundo = 2000
alto_mundo = 2000

# ------- VARIABLES DE JUEGO --------

modo_juego = "local"


jugador : Serpiente

bots = []
serpientes = []

puntos = []

CANTIDAD_JUGADORES_MIN = 12


COLORES_SERPIENTES = {
    "rojo": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255),
    "amarillo": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cian": (0, 255, 255),
    "naranja": (255, 128, 0),
    "violeta": (128, 0, 255),
    "celeste fuerte": (0, 128, 255),
    "verde agua": (0, 255, 128),
    "rosa fuerte": (255, 0, 128),
    "verde lima": (128, 255, 0),
    "rosa claro": (255, 200, 200),
    "verde claro": (200, 255, 200),
    "azul claro": (200, 200, 255),
}

CANTIDAD_INCIAL_PUNTOS = 500

running = True

running_menu = True


pygame.init()
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
clock = pygame.time.Clock()

# ------- EVENTOS ---------




bg_image = pygame.image.load("imagenes/fondo_juego.png")

def SpawnearPuntos(cantidad):
    for i in range(cantidad):
        puntos.append(Punto(ancho_mundo, alto_mundo))


def dibujarFondo(cam_x, cam_y):

    global bg_image
    
    screen.fill((0,0,0))
    
    """


    
    bg_w, bg_h = bg_image.get_size()
    bg_w, bg_h = bg_w*4, bg_h*4

    bg = pygame.transform.scale(bg_image, (bg_w, bg_h))


    

    start_x = -cam_x % bg_w
    start_y = -cam_y % bg_h

    for x in range(-bg_w, ancho_pantalla + bg_w, bg_w):
        for y in range(-bg_h, alto_pantalla + bg_h, bg_h):
            screen.blit(bg, (start_x + x, start_y + y))
    """

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
    """
    bg = pygame.transform.scale(bg_image, (ancho_pantalla, alto_pantalla))
    screen.blit(bg, (0,0))
    """
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

def obtenerPosicionSpawn():

    global jugador

    pos_valida = False

    pos_bot_x : pygame.Vector2
    pos_bot_y : pygame.Vector2

    while not pos_valida:
        pos_bot_x, pos_bot_y = random.randint(50, ancho_mundo - 50), random.randint(50, alto_mundo - 50)


        serpientes = bots.copy()
        serpientes.append(jugador)
        for serpiente in serpientes:
            if isinstance(serpiente, Serpiente):
                radio =  math.dist(serpiente.pos, serpiente.segmentos[-1]) / 2
                cx = (serpiente.pos.x + serpiente.segmentos[-1].x) / 2
                cy = (serpiente.pos.y + serpiente.segmentos[-1].y) / 2

                distancia = math.dist((pos_bot_x, pos_bot_y), (cx, cy))

                if distancia < radio + 20:
                    break
        else:
            pos_valida = True

    return pos_bot_x, pos_bot_y
    
def startLocalGame():

    SpawnearPuntos(CANTIDAD_INCIAL_PUNTOS)

    global jugador, bots

    lista_colores = list(COLORES_SERPIENTES.values())
    lista_nombres = list(COLORES_SERPIENTES.keys())

    # --- Crear jugador ---
    indice = random.randint(0, len(lista_colores)-1)
    color_elegido = lista_colores[indice]
    nombre_color = lista_nombres[indice]

    jugador = Serpiente(300, 200, nombre_color, color_elegido)
    serpientes.append(jugador)

    # Para que no se repita (opcional):
    lista_colores.pop(indice)
    lista_nombres.pop(indice)

    # --- Crear bots ---
    for i in range(CANTIDAD_JUGADORES_MIN - 1):

        pos_x, pos_y = obtenerPosicionSpawn()

        indice = random.randint(0, len(lista_colores)-1)
        color_elegido = lista_colores[indice]
        nombre_color = lista_nombres[indice]

        clase_bot = random.choice(clases_bots)
        bot = clase_bot(pos_x, pos_y, nombre_color, color_elegido)

        bots.append(bot)
        serpientes.append(bot)

        # Para evitar repetidos (opcional):
        lista_colores.pop(indice)
        lista_nombres.pop(indice)


def onMuerteSerpiente(serpiente: Serpiente):


    segmentos = [seg.copy() for seg in serpiente.segmentos]

    cantidad_puntos = 0

    puntos_totales = serpiente.contador_puntos_consumidos

    while cantidad_puntos < puntos_totales:
        pos = random.choice(segmentos)
        segmentos.remove(pos)

        punto = Punto(ancho_mundo, alto_mundo, pygame.Vector2(pos.x, pos.y))
        cantidad_puntos += punto.size
        puntos.append(punto)




while running:

    dt = clock.get_time() / 1000

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
                    jugador.sprint = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                if not running_menu:
                    jugador.sprint = False



    

    if running_menu: # si esta en el menu hace unicamente lo del menu

        dibujarMenu()

        pygame.display.flip()
        clock.tick(60)
        continue


    if isinstance(jugador, Serpiente):
        


        cam_x = jugador.pos.x - ancho_pantalla // 2
        cam_y = jugador.pos.y - alto_pantalla // 2

        if col.colision_jugador_vs_bots(jugador, bots):
            running = False

        bot_muerto = col.colision_bots_vs_jugador(jugador, bots)
        if bot_muerto:
            onMuerteSerpiente(bot_muerto)
            bots.remove(bot_muerto)
            serpientes.remove(bot_muerto)

        bots_muertos = col.colision_bots_vs_bots(bots)
        for b in bots_muertos:
            if b in bots:
                onMuerteSerpiente(b)
                bots.remove(b)
                serpientes.remove(b)

        col.colision_jugador_puntos(jugador, puntos)
        col.colision_bots_puntos(bots, puntos)

        dibujarFondo(cam_x, cam_y)

        dibujarPuntosNuevos(cam_x, cam_y)
    

        for bot in bots:

            bot.actualizar(dt, serpientes, puntos, jugador)
            bot.dibujar(screen, cam_x, cam_y)

        jugador.set_direccion_con_mouse()
        jugador.actualizar(dt)

        jugador.dibujar(screen, cam_x, cam_y)
        
        UI.dibujar_leaderboard(screen, serpientes, ancho_pantalla -250, 50)






    # RENDER YOUR GAME HERE


    pygame.display.flip()

    clock.tick(60)

pygame.quit()