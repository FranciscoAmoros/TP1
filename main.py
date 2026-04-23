import pygame

from puntos import Punto

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

ancho_pantalla = 1200
alto_pantalla = 800

MAP_RADIUS = 2000
CENTER = (2000, 2000)

# ------- VARIABLES DE JUEGO --------

modo_juego = "local"

game_over = False
gano = False
boton_final = None


jugador : Serpiente

bots = []
serpientes = []

puntos = []

CANTIDAD_JUGADORES_MIN = 20

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

    "gris": (120, 120, 120),
    "gris claro": (200, 200, 200),
    "gris oscuro": (60, 60, 60),
    "marron": (139, 69, 19),
    "oro": (255, 215, 0),
    "turquesa": (64, 224, 208),
    "lavanda": (230, 230, 250),
    "salmon": (250, 128, 114),
    "azul marino": (0, 0, 128),
    "verde oscuro": (0, 100, 0),
}

CANTIDAD_INCIAL_PUNTOS = 2200

running = True

running_menu = True


pygame.init()
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
clock = pygame.time.Clock()

# ------- EVENTOS ---------




bg_image = pygame.image.load("imagenes/fondo sliher.jpg")
tamaño_bg_image_x, tamaño_bg_image_y = bg_image.get_size()
tamaño_bg_image_x, tamaño_bg_image_y = tamaño_bg_image_x * 4, tamaño_bg_image_y * 4
bg_image_scaled = pygame.transform.scale(bg_image, (tamaño_bg_image_x, tamaño_bg_image_y))

def SpawnearPuntos(cantidad):
    for i in range(cantidad):
        puntos.append(Punto(MAP_RADIUS, CENTER))


def dibujarFondo(cam_x, cam_y):

    global bg_image_scaled
    
    screen.fill((0,0,0))
    


    
    bg_w, bg_h = bg_image_scaled.get_size()

    start_x = -cam_x % bg_w
    start_y = -cam_y % bg_h

    for x in range(-bg_w, ancho_pantalla + bg_w, bg_w):
        for y in range(-bg_h, alto_pantalla + bg_h, bg_h):
            screen.blit(bg_image_scaled, (start_x + x, start_y + y))

    pygame.draw.circle(
    screen,
    (255, 0, 0),
    (int(CENTER[0] - cam_x), int(CENTER[1] - cam_y)),
    MAP_RADIUS,
    5
)

def dibujarPuntosNuevos(cam_x, cam_y):
    for p in puntos:
        p.draw(screen, cam_x, cam_y)

# ---- MENU -------

botones = []

botones = []

boton_jugar = UI.Boton("JUGAR", ancho_pantalla//2 - 150, alto_pantalla//2, 300, 70)
boton_salir = UI.Boton("SALIR", ancho_pantalla//2 - 150, alto_pantalla//2 + 100, 300, 70)

botones.append(boton_jugar)
botones.append(boton_salir)


def dibujarMenu():
    
    global bg_image_scaled

    bg_w, bg_h = bg_image_scaled.get_size()


    for x in range(-bg_w, ancho_pantalla + bg_w, bg_w):
        for y in range(-bg_h, alto_pantalla + bg_h, bg_h):
            screen.blit(bg_image_scaled, (x, y))


    boton_jugar.dibujar(screen)
    boton_salir.dibujar(screen)

def onClicked(boton="salir"):
    global running, running_menu

    if boton == "salir":
        running = False

    if boton == "jugar":
        running_menu = False
        startLocalGame()



def obtenerPosicionSpawn():

    global jugador

    pos_valida = False

    while not pos_valida:

        angle = random.uniform(0, 2 * math.pi)
        r = (MAP_RADIUS - 50) * math.sqrt(random.random())

        pos_bot_x = CENTER[0] + r * math.cos(angle)
        pos_bot_y = CENTER[1] + r * math.sin(angle)

        serpientes = bots.copy()
        serpientes.append(jugador)

        for serpiente in serpientes:
            if isinstance(serpiente, Serpiente):

                radio = math.dist(serpiente.pos, serpiente.segmentos[-1]) / 2
                cx = (serpiente.pos.x + serpiente.segmentos[-1].x) / 2
                cy = (serpiente.pos.y + serpiente.segmentos[-1].y) / 2

                distancia = math.dist((pos_bot_x, pos_bot_y), (cx, cy))

                if distancia < radio + 20:
                    break
        else:
            pos_valida = True

    return pos_bot_x, pos_bot_y

def resetJuego():
    global bots, serpientes, puntos, jugador

    bots.clear()
    serpientes.clear()
    puntos.clear()
    jugador = None
    
def startLocalGame():

    SpawnearPuntos(CANTIDAD_INCIAL_PUNTOS)

    global jugador, bots

    lista_colores = list(COLORES_SERPIENTES.values())
    lista_nombres = list(COLORES_SERPIENTES.keys())

    indice = random.randint(0, len(lista_colores)-1)
    color_elegido = lista_colores[indice]
    nombre_color = lista_nombres[indice]

    jugador = Serpiente(300, 200, nombre_color, CENTER, MAP_RADIUS, color_elegido)
    serpientes.append(jugador)


    lista_colores.pop(indice)
    lista_nombres.pop(indice)

    for i in range(CANTIDAD_JUGADORES_MIN - 1):

        pos_x, pos_y = obtenerPosicionSpawn()

        indice = random.randint(0, len(lista_colores)-1)
        color_elegido = lista_colores[indice]
        nombre_color = lista_nombres[indice]

        # 🎯 DISTRIBUCIÓN DE TIPOS
        r = random.random()

        if r < 0.6:
            clase_bot = SerpienteAgresiva
        elif r < 0.8:
            clase_bot = SerpienteMiedosa
        else:
            clase_bot = SerpienteComePuntos

        bot = clase_bot(pos_x, pos_y, nombre_color, CENTER, MAP_RADIUS, color_elegido)

        bots.append(bot)
        serpientes.append(bot)

        lista_colores.pop(indice)
        lista_nombres.pop(indice)


def onMuerteSerpiente(serpiente: Serpiente):


    segmentos = [seg.copy() for seg in serpiente.segmentos]

    cantidad_puntos = 0

    puntos_totales = serpiente.contador_puntos_consumidos

    while cantidad_puntos < puntos_totales:
        pos = random.choice(segmentos)
        segmentos.remove(pos)

        punto = Punto(MAP_RADIUS, CENTER, pygame.Vector2(pos.x, pos.y))
        cantidad_puntos += punto.size
        puntos.append(punto)

    """
    distancias_bots = []

    for bot in bots:
        if bot is serpiente:
            continue

        dist = bot.pos.distance_to(serpiente.pos)
        distancias_bots.append((dist, bot))

    distancias_bots.sort(key=lambda x: x[0])

    dos_mas_cercanas = distancias_bots[:2]

    for distancia, bot_cercano in dos_mas_cercanas:
        bot_cercano.onMuerteSerpiente(distancia, serpiente.pos)
    """






while running:

    dt = clock.get_time() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if running_menu:
                for b in botones:
                    if b.clickeado(event.pos):
                        onClicked(b.texto.lower())

            elif game_over and boton_final:
                if boton_final.clickeado(event.pos):
                    resetJuego()
                    running_menu = True
                    game_over = False

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

    if game_over:
        boton_final = UI.dibujar_pantalla_final(
            screen,
            gano,
            jugador.contador_puntos_consumidos if jugador else 0,
            ancho_pantalla,
            alto_pantalla
        )
        pygame.display.flip()
        clock.tick(60)
        continue


    if isinstance(jugador, Serpiente):
        


        cam_x = jugador.pos.x - ancho_pantalla // 2
        cam_y = jugador.pos.y - alto_pantalla // 2

        if col.colision_jugador_vs_bots(jugador, bots):
            onMuerteSerpiente(jugador)
            serpientes.remove(jugador)
            game_over = True
            gano = False

        bot_muerto = col.colision_bots_vs_jugador(jugador, bots)
        if bot_muerto:
            onMuerteSerpiente(bot_muerto)
            bots.remove(bot_muerto)
            serpientes.remove(bot_muerto)

            if len(bots) == 0:
                game_over = True
                gano = True

        bots_muertos = col.colision_bots_vs_bots(bots)
        for b in bots_muertos:
            if b in bots:
                onMuerteSerpiente(b)
                bots.remove(b)
                serpientes.remove(b)

                if len(bots) == 0:
                    game_over = True
                    gano = True

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