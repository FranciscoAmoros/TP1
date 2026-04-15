import pygame

def colisiones_circulos(x1, y1, r1, x2, y2, r2): # funcion que detecta las collisiones entre cirulos

    return (x1 - x2)**2 + (y1 - y2)**2 <= (r1 + r2)**2 # midiendo la distancia y el radio

def colision_jugador_vs_bots(jugador, bots):
    head_x, head_y, head_r = jugador.get_head_hitbox()

    for bot in bots:
        for bx, by, br in bot.get_body_hitboxes():
            if colisiones_circulos(head_x, head_y, head_r, bx, by, br):
                return True  # jugador muere

    return False

def colision_bots_vs_jugador(jugador, bots):
    head_x, head_y, head_r = jugador.get_head_hitbox()

    for bot in bots:
        bx, by, br = bot.get_head_hitbox()

        for jx, jy, jr in jugador.get_body_hitboxes():
            if colisiones_circulos(bx, by, br, jx, jy, jr):
                return bot  # el bot muere

    return None

def colision_bots_vs_bots(bots):
    muertos = []

    for i, bot in enumerate(bots):
        bx, by, br = bot.get_head_hitbox()

        for j, otro in enumerate(bots):
            if i == j:
                continue

            for ox, oy, orad in otro.get_body_hitboxes():
                if colisiones_circulos(bx, by, br, ox, oy, orad):
                    muertos.append(bot)
                    break

    return muertos

def colision_bots_puntos(bots, puntos):
    for bot in bots:
        bx, by, br = bot.get_head_hitbox()

        for p in puntos[:]:
            if colisiones_circulos(bx, by, br, p.x, p.y, p.size):
                bot.crecer(p.size)
                puntos.remove(p)

def colision_jugador_puntos(jugador, puntos):
    head_x, head_y, head_r = jugador.get_head_hitbox()

    for p in puntos[:]:
        if colisiones_circulos(head_x, head_y, head_r, p.x, p.y, p.size):
            jugador.crecer(p.size)
            puntos.remove(p)