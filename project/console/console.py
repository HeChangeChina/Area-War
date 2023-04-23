from display.display_object import DisplayObject
from console.unit_shower import UnitShower
from console.resource_shower import ResourceShower
from console.army_button import ArmyButton
import pygame


class Console(DisplayObject):
    def __init__(self):
        super().__init__()

        self.unit_shower = UnitShower()
        self.resource_shower = ResourceShower()
        self.army_button_list = list()
        key_dict = {1: pygame.K_1, 2: pygame.K_2, 3: pygame.K_3, 4: pygame.K_4, 5: pygame.K_5, 6: pygame.K_6,
                    7: pygame.K_7, 8: pygame.K_8, 9: pygame.K_9, 0: pygame.K_0}
        for i in range(1, 10):
            button = ArmyButton(50 + (i - 1) * 60, key_dict[i], self.unit_shower, str(i))
            self.army_button_list.append(button)
        button = ArmyButton(590, key_dict[0], self.unit_shower, "0")
        self.army_button_list.append(button)

        self.message_require("update_60", self.update)

    def mouse_right_target(self, data):
        self.unit_shower.mouse_right_target(data)

    def use_skill(self, skill, data):
        self.unit_shower.use_skill(skill, data)

    def use_skill_by_flag(self, skill_flag, data):
        self.unit_shower.use_skill_by_flag(skill_flag, data)

    def update(self, data):
        self.unit_shower.update()
        self.resource_shower.update()

    def set_units(self, units):
        self.unit_shower.choose_units(units)

    def get_surface(self):
        surface_list = list()
        # surface_list.append([self.surface, self.c_rect])
        for i in self.unit_shower.get_surface():
            surface_list.append(i)
        for i in self.resource_shower.get_surface():
            surface_list.append(i)
        for i in self.army_button_list:
            surface_list.append(i.get_surface())
        return surface_list

    def clear(self):
        super().clear()
        self.unit_shower.clear()
        self.resource_shower.clear()
        for i in self.army_button_list:
            i.clear()

        self.unit_shower = None
        self.resource_shower = None
        self.army_button_list = list()
