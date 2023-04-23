from base import Base
from display.atlas import Atlas
from display.font import FontSurface
import pygame


class CloseUp(Base):
    def __init__(self):
        super().__init__()
        self.unit = None
        self.surface = pygame.Surface((150, 270))
        self.c_rect = pygame.Rect(340, 810, 150, 270)
        self.frame = Atlas.load("./data/img/console", "CloseUp")
        self.background = Atlas.load("./data/img/console", "CloseUpBG")

        self.surface.set_colorkey((0, 0, 0))

        self.health = None
        self.magic = None
        self.health_rect = pygame.Rect(0, 1000, 200, 40)
        self.magic_rect = pygame.Rect(0, 1045, 200, 40)
        self.close_up = None
        self.close_up_rect = pygame.Rect(0, 0, 300, 300)

        self.f_frame = dict()
        self.f_frame["defeat"] = pygame.Surface((150, 270))
        self.f_frame["defeat"].set_colorkey((0, 0, 0))
        self.f_frame["defeat"].blit(self.background["defeat"][0][0], [13, 15])
        self.f_frame["defeat"].blit(self.frame["defeat"][0][0], [0, 0])

    def set_unit(self, unit):
        self.unit = unit

    def get_surface(self):
        if self.health is None or self.magic is None or self.close_up is None:
            return [[self.surface, self.c_rect]]
        else:
            return [[self.surface, self.c_rect], [self.close_up, self.close_up_rect], [self.health, self.health_rect],
                    [self.magic, self.magic_rect]]

    def update(self):
        if self.unit is not None:
            if self.unit.wait_to_death:
                self.unit = None
                return
            self.surface = self.f_frame[self.unit.unit_panel["close_up_background"]]
            self.close_up = self.unit.shader.get_surface()
            height_c = self.unit.unit_height_c
            if self.close_up.get_width() > 150:
                width = self.close_up.get_width()
                self.close_up = pygame.transform.scale(self.close_up, (150, int(self.close_up.get_height() * 150 /
                                                                                self.close_up.get_width())))
                height_c *= 150 / width
            if self.close_up.get_height() > 135:
                height = self.close_up.get_height()
                self.close_up = pygame.transform.scale(self.close_up, (int(self.close_up.get_width() * 135 /
                                                                           self.close_up.get_height()), 135))
                height_c *= 135 / height
            self.close_up_rect.left = 75 - self.close_up.get_width() / 2 + self.c_rect.left
            self.close_up_rect.top = 144 - height_c + self.c_rect.top

            health_s = str(int(self.unit.attribute_manager.health)) + "/" + str(self.unit.attribute_manager.
                                                                                attribute_dict["max_health"])
            health = FontSurface(text=health_s, size=16, color=(200, 230, 200)).surface
            health_x = (150 - health.get_width()) / 2
            self.health = health
            self.health_rect.left = health_x + self.c_rect.left

            magic_s = str(int(self.unit.attribute_manager.magic)) + "/" + str(self.unit.attribute_manager.
                                                                               attribute_dict["max_magic"])
            magic = FontSurface(text=magic_s, size=16, color=(230, 200, 230)).surface
            magic_x = (150 - magic.get_width()) / 2
            self.magic = magic
            self.magic_rect.left = magic_x + self.c_rect.left
        else:
            self.surface = self.f_frame["defeat"]
            self.close_up = None
            self.health = None
            self.magic = None

    def clear(self):
        super().clear()
        self.unit = None
