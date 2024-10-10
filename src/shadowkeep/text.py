import pygame


class TextInput():
    def __init__(self, game):
        self.game = game
        self.is_open = False
        self.text = "Ahoj"
        self.surface = pygame.surface.Surface((250, 150))
        self.font = pygame.font.Font(None, 14)

    def blit(self):
        if self.is_open:
            self.surface.fill((255, 255, 255))
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            self.surface.blit(text_surface, (10, 10))
            self.game.ui_layer.place_surface(
                self.surface, (20, 20)
            )

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN]:
            self.is_open = False
        elif pressed_keys[pygame.K_ESCAPE]:
            self.text = ""
        elif pressed_keys[pygame.K_BACKSPACE]:
            if self.text:
                self.text = self.text[:-1]
        else:
            self.text += event.unicode

# textwrap(text, sirku) .... rozdeli text na radky
