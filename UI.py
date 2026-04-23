import pygame


pygame.font.init()

font_grande = pygame.font.SysFont("Arial", 72)
font_mediana = pygame.font.SysFont("Arial", 40)

class BotonUI:
    def __init__(self, texto, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto

        self.color_normal = (40, 40, 40)
        self.color_hover = (70, 70, 70)
        self.color_borde = (200, 200, 200)

        self.font = pygame.font.SysFont("Arial", 36)

    def dibujar(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_normal

        # sombra
        sombra = self.rect.move(4, 4)
        pygame.draw.rect(screen, (0, 0, 0), sombra, border_radius=10)

        # botón
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, self.color_borde, self.rect, 2, border_radius=10)

        txt = self.font.render(self.texto, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clickeado(self, pos):
        return self.rect.collidepoint(pos)

class BotonSimple:
    def __init__(self, texto, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto

    def dibujar(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)

        txt = font_mediana.render(self.texto, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clickeado(self, pos):
        return self.rect.collidepoint(pos)


def dibujar_pantalla_final(screen, gano, puntaje, ancho, alto):
    
    # Fondo oscuro
    overlay = pygame.Surface((ancho, alto))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Texto principal
    texto = "GANASTE" if gano else "PERDISTE"
    color = (0, 255, 0) if gano else (255, 0, 0)

    titulo = font_grande.render(texto, True, color)
    screen.blit(titulo, titulo.get_rect(center=(ancho//2, alto//3)))

    # Puntaje
    puntaje_txt = font_mediana.render(f"Puntaje: {puntaje}", True, (255,255,255))
    screen.blit(puntaje_txt, puntaje_txt.get_rect(center=(ancho//2, alto//2)))

    # Botón
    boton = BotonSimple("Volver al menú", ancho//2 - 150, alto//2 + 80, 300, 60)
    boton.dibujar(screen)

    return boton

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
        
