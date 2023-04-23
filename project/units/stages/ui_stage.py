import pygame
from display.stage import Stage
from display.font import Font
from display.cursor import Cursor


class UIStage(Stage):
    def __init__(self, father_surface):
        super().__init__(0, 0, 200, 200, father_surface)
        self.surface.set_colorkey((0, 0, 0))
        self.set_sky_box((0, 0, 0))
        self.font = Font("60", 25, pygame.Rect(25, 25, 300, 50))
        self.print_font = Font("NonePrint", 25, pygame.Rect(25, 80, 300, 50))
        self.add(self.font)
        self.add(self.print_font)
        self.cursor = Cursor()
        self.add(self.cursor, 100)
        self.clear_rect.append(pygame.Rect(25, 25, 300, 130))
        self.clear_rect.append(pygame.Rect(500, 500, 50, 50))

        self.message_require("print_on_screen", self.print_data)

    def before_draw(self):
        self.clear_rect[1] = self.cursor.c_rect

    def print_data(self, data):
        self.print_font.change_text(data)

    def set_frame(self, frame):
        self.font.change_text("fps:" + str(frame))

