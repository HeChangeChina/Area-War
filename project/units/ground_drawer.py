from display.display_object import DisplayObject

import pygame


class GroundDrawer(DisplayObject):
    def __init__(self, length=7680):
        super().__init__()
        self.surface = pygame.Surface((length, 20)).convert_alpha()
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))
        self.length = length
        self.rect = pygame.Rect(-length / 2, 800, length, 20)
        self.shadow_list = []
        self.ellipse_list = []
        self.message_require("shadow_draw", self.add_shadow)
        self.message_require("ellipse_draw", self.add_ellipse)
        self.message_require("update_60", self.update)

    def add_ellipse(self, data):
        self.ellipse_list.append(data)

    def add_shadow(self, data):
        self.shadow_list.append(data)

    def update(self, data):
        self.surface.fill((0, 0, 0))
        for i in self.shadow_list:
            rect = pygame.Rect(self.length / 2 + i[0] - i[1], 1, i[1] * 2, 10)
            # print(rect)
            alpha = 150
            if len(i) == 3:
                alpha = i[2]
            pygame.draw.ellipse(self.surface, (80, 80, 130, alpha), rect)
        self.shadow_list = []

        for i in self.ellipse_list:
            hr = 3.5 if len(i) == 4 else i[4]
            rect = pygame.Rect(self.length / 2 + i[0] - i[1], 5.5 - hr, i[1] * 2, 5.5 + hr)
            pygame.draw.ellipse(self.surface, (80, 80, 80), rect, width=1)
            rect = pygame.Rect(self.length / 2 + i[0] - i[1], 4.5 - hr, i[1] * 2, 4.5 + hr)
            pygame.draw.ellipse(self.surface, i[2], rect, width=i[3])
        self.ellipse_list = []

    def get_surface(self):
        return [[self.surface, self.rect]]


