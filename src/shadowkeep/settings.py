import sys
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)

pygame.init()
font = pygame.font.Font(None, 32)


class Button:
    def __init__(self, game, x, y, width, height, text):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(self.game.window, GREY, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        pygame.display.flip()

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.text == "Increase Volume":
            self.increase_volume()
        elif self.text == "Decrease Volume":
            self.decreace_volume()

    def increase_volume(self):
        if self.game.audio.global_volume < 1.5:
            self.game.audio.global_volume += 0.05
            self.game.audio.set_volume(self.game.audio.global_volume)

    def decreace_volume(self):
        if self.game.audio.global_volume > 0.04:
            self.game.audio.global_volume -= 0.05
            self.game.audio.set_volume(self.game.audio.global_volume)
