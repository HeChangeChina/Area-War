from base import Base
import pygame


class ProjectionDrawer(Base):
    def __init__(self):
        super().__init__()
        self.p_rect = []
        self.camera = 0
        self.message_require("projection_draw", self.add)
        self.message_require("update_60", self.clear_list)

    def draw(self, surface_list):
        rect = surface_list[1]
        if rect.left + self.camera > 1920 or rect.left + rect.width + self.camera < 0:
            return surface_list
        p_rect_list = []
        for i in range(len(self.p_rect)):
            p_rect_list.append(self.p_rect[i][0])
        c_list = rect.collidelistall(p_rect_list)
        if len(c_list) > 0:
            surface = surface_list[0].copy()
            for i in c_list:
                c_rect = self.p_rect[i][0].clip(rect)
                c_rect.left -= rect.left
                c_rect.top -= rect.top
                strength = 1 - self.p_rect[i][1] / 255
                surface.fill((160 + 95 * strength, 160 + 95 * strength, 220 + 35 * strength), rect=c_rect,
                             special_flags=pygame.BLEND_RGB_MULT)
            return [surface, rect]
        else:
            return surface_list

    def add(self, data):
        self.p_rect.append(data)

    def clear_list(self, data):
        self.p_rect = []
