import pygame
import textwrap


class TextInput:
    def __init__(self, game):
        self.game = game
        self.is_open = False
        self.text1 = "Jake je heslo"
        self.text2 = ""
        self.bg_surface = pygame.surface.Surface((250, 150))
        self.font_size = 20
        self.line_height = round(self.font_size * 0.9)
        self.font = pygame.font.Font(None, self.font_size)
        self.maximum_letters = 250 / 18
        self.text_position = (10, 10)
        self.backspace_timer = 0
        self.backspace_pressed = False

    def surface_set(self, bg_surface, text, font, position):
        self.bg_surface.fill((255, 255, 255))
        wrapped_text = textwrap.wrap(text, width=32)

        for line in wrapped_text:
            text_surface = font.render(line, True, (0, 0, 0))
            bg_surface.blit(text_surface, (position))
            position = (position[0], position[1] + self.line_height)

        return bg_surface

    def blit(self):
        if self.is_open:
            self.surface1 = self.surface_set(
                self.bg_surface, self.text1, self.font, (10, 10)
            )
            self.game.ui_layer.place_surface(self.surface1, (20, 200))
            self.surface2 = self.surface_set(
                self.bg_surface, self.text2, self.font, (10, 10)
            )
            self.game.ui_layer.place_surface(self.surface2, (500, 200))

    def read_key(self, event):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN]:
            self.is_open = False
            if self.text2 != "jablko":
                self.game.running = False
            self.text2 = ""
        elif pressed_keys[pygame.K_ESCAPE]:
            self.text2 = ""
            self.is_open = False
        elif pressed_keys[pygame.K_BACKSPACE]:
            self.text2 = self.text2[:-1]
            self.backspace_pressed = True
            self.backspace_timer = pygame.time.get_ticks()
        else:
            self.text2 += event.unicode

    def backspace_update(self):
        if self.backspace_pressed:
            if pygame.time.get_ticks() - self.backspace_timer > 80:
                self.text2 = self.text2[:-1]
                self.backspace_timer = pygame.time.get_ticks()

        if not pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            self.backspace_pressed = False
