import pygame

import pygame

def dibujar_leaderboard(pantalla, serpientes, x, y):

    font = pygame.font.SysFont("arial", 18)
    altura_fila = 22
    max_items = 10

    serpientes_ordenadas = sorted(
        serpientes,
        key=lambda s: s.contador_puntos_consumidos,
        reverse=True
    )[:max_items]

    ancho = 180 
    alto = altura_fila * len(serpientes_ordenadas) + 6

    surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 90)) 

    pantalla.blit(surface, (x, y))

    for i, serpiente in enumerate(serpientes_ordenadas):
        fila_y = y + 3 + i * altura_fila

        pygame.draw.rect(
            pantalla,
            serpiente.color,
            (x + 6, fila_y + 3, 14, 14)
        )

        txt_nombre = font.render(serpiente.nombre, True, (255, 255, 255))
        pantalla.blit(txt_nombre, (x + 24, fila_y + 2))

        txt_puntaje = font.render(str(serpiente.contador_puntos_consumidos), True, (255, 255, 0))
        r = txt_puntaje.get_rect()
        r.topright = (x + ancho - 8, fila_y + 2)
        pantalla.blit(txt_puntaje, r)
        
