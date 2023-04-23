from display.shader import Shader
from auxiliary_tools.flag_manager import FlagManager
from display.display_object import DisplayObject
import pygame


class Font(DisplayObject):
    def __init__(self, text, size, c_rect, color=(255, 255, 255)):
        super().__init__()
        self.shader = Shader()
        self.text = text
        self.size = size
        self.color = color
        self.c_rect = c_rect
        self.if_clear = False
        self.font = pygame.font.Font("./data/ipix_font.ttf", size)
        self.surface = self.font.render(self.text, False, self.color)
        self.shader.set_surface(self.surface)
        self.flag = FlagManager()

        self.update_text()

    def change_text(self, text):
        self.text = text
        self.update_text()

    def update_text(self):
        self.surface = self.font.render(self.text, False, self.color)
        self.shader.set_surface(self.surface)

    def get_surface(self):
        return [[self.shader.get_surface(), self.c_rect]]

    def clear(self):
        super().clear()
        self.if_clear = True


class FontSurface:
    def __init__(self, text, size, color=(255, 255, 255)):
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.Font("./data/ipix_font.ttf", size)
        self.surface = None

        self.update_text()

    def change_text(self, text):
        self.text = text
        self.update_text()

    def update_text(self):
        self.surface = self.font.render(self.text, False, self.color)


class StaticFontSurface:
    @classmethod
    def get(cls, text, size, color=(255, 255, 255), width=150):
        font = pygame.font.Font("./data/ipix_font.ttf", size)
        text_list = list()
        now_text = ""
        for i in range(len(text)):
            now_text += text[i]
            if font.size(now_text)[0] > width or text[i] == "&":
                text_list.append(now_text[:-1])
                if text[i] != "&":
                    now_text = text[i]
                else:
                    now_text = ""
        if len(now_text) > 1:
            text_list.append(now_text)

        text_lineheight = font.get_height() * 1.35
        surface = pygame.Surface((width, text_lineheight * len(text_list)))
        surface.set_colorkey((0, 0, 0))
        for i in range(len(text_list)):
            line_surface = font.render(text_list[i], False, color)
            surface.blit(line_surface, [0, i * text_lineheight])

        return surface

