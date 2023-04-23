from display.display_object import DisplayObject
from display.atlas import Atlas
from auxiliary_tools.exact_rect import ERect
from auxiliary_tools.message_manager import MessageManager
import pygame


class Background(DisplayObject):
    def __init__(self, img_group, img, style, c_rect, move_speed=0, last_time=0, shadow_size=0, shadow_c=0):
        super().__init__()
        self.surface = Atlas.load("./data/img/background", img_group)[img][style][0].copy()
        self.alpha = 255
        self.move_speed = move_speed / 60
        self.move_total = 0
        self.c_rect = ERect()
        self.c_rect.load_rect(c_rect)
        self.shadow_size = shadow_size
        self.shadow_c = shadow_c

        self.last_time = last_time
        if last_time > 0:
            self.alpha = 0
            self.surface.set_alpha(self.alpha)
            self.last_time = last_time * 60
            self.message_require("update_60", self.update)

    def update(self, data):
        self.c_rect.left += self.move_speed
        # print(self.last_time)
        if self.last_time <= 0:
            self.alpha -= 5
            if self.alpha <= 0:
                self.clear()
                return
            self.surface.set_alpha(self.alpha)
        elif self.alpha != 255:
            self.alpha += 5
            self.surface.set_alpha(self.alpha)

        if self.shadow_size > 0 and self.in_screen:
            c_rect = self.c_rect.rect()
            center = c_rect.left + c_rect.width / 2 + self.shadow_c
            MessageManager.send_message("shadow_draw", [center, self.shadow_size])

        if self.shadow_size > 0 and self.in_screen:
            c_rect = self.c_rect.rect()
            center = c_rect.left + c_rect.width / 2 + self.shadow_c
            projection_rect = pygame.Rect(center - self.shadow_size, c_rect.top, self.shadow_size * 2, 1080)
            strength = int(self.alpha * 150 / 255)
            MessageManager.send_message("projection_draw", [projection_rect, strength])

        self.last_time -= 1

    def get_surface(self):
        return [[self.surface, self.c_rect.rect()]]

    def clear(self):
        super().clear()
        self.if_clear = True
        self.surface = None
        self.alpha = None
        self.move_speed = None
        self.last_time = None
