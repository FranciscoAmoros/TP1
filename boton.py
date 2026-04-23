import pygame

class Boton:
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

        sombra = self.rect.move(4, 4)
        pygame.draw.rect(screen, (0, 0, 0), sombra, border_radius=12)

        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, self.color_borde, self.rect, 2, border_radius=12)

        txt = self.font.render(self.texto.upper(), True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clickeado(self, pos):
        return self.rect.collidepoint(pos)