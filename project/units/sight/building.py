from unit_tools.sight import Sight
from units.ground import Ground
from auxiliary_tools.building_gird import BuildingGird
import pygame


class BuildingSight(Sight):
    def __init__(self, atlas, height_c, width, gird_layer):
        super().__init__(atlas, "./data/img/units/buildings/" + atlas)
        self.show_mode = 1
        self.width = width
        self.height_c = height_c
        self.gird_layer = gird_layer

        self.blue_building = self.atlas["defeat"][0][0].copy()
        self.red_building = self.atlas["defeat"][0][0].copy()

        self.blue_building.fill((155, 155, 255), special_flags=pygame.BLEND_RGB_MULT)
        self.red_building.fill((255, 155, 155), special_flags=pygame.BLEND_RGB_MULT)

    def start_draw(self):
        self.c_rect.width = self.width
        self.c_rect.height = self.blue_building.get_width()
        self.c_rect.top = 800 - self.height_c

    def draw(self, target):
        x = target[0] - self.width / 2 if type(target) is tuple or type(target) is list \
            else target.c_rect.left + target.c_rect.width / 2
        left_gird = (Ground.length / 2 + x) // 50
        sight_x = -Ground.length / 2 + left_gird * 50
        gird_list = list()
        for i in range(self.c_rect.width // 51 + 1):
            gird_list.append(int(left_gird + i))

        have_building = not BuildingGird.check_gird(gird_list, self.gird_layer)
        self.surface = self.red_building if have_building else self.blue_building
        self.c_rect.x = sight_x

