import pygame
from display.display_object import DisplayObject
from display.atlas import Atlas
from auxiliary_tools.building_gird import BuildingGird


class Ground(DisplayObject):
    length = 0

    def __init__(self, length=7680):
        super().__init__()
        __class__.length = length
        self.rect = pygame.Rect(-length / 2, 800, length, 280)
        self.day_time_surface = pygame.Surface((length, 280)).convert()
        self.ground_atlas = Atlas.load("./data/img/ground", "ground")
        self.if_clear = False
        # print(self.ground_atlas)
        BuildingGird.reset_gird(int(length / 50) + 1)
        for i1 in range(int(length / 50) + 1):
            for i2 in range(6):
                rect = pygame.Rect(i1 * 50, i2 * 50, 50, 50)
                if i2 == 0:
                    self.day_time_surface.blit(self.ground_atlas["grasslandD"][0][0], rect)
                else:
                    self.day_time_surface.blit(self.ground_atlas["grasslandD"][1][0], rect)
            s_rect = pygame.Rect(i1 * 50, 200, 50, 100)
            self.day_time_surface.blit(self.ground_atlas["shadow"][0][0], s_rect)

    def get_surface(self):
        return [[self.day_time_surface, self.rect]]
