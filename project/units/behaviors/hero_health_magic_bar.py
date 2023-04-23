from unit_tools.behavior import Behavior
from display.atlas import Atlas
from display.font import Font
import pygame


class HeroHMBar(Behavior):
    def __init__(self, width=1.25, cell_amount="auto", name="hero", name_c=0, height_c=0):
        super().__init__()
        self.flag.add_flag(["HMBar", "info_show"])
        self.width = width
        self.cell_amount = cell_amount
        self.name = name
        self.name_c = name_c
        self.chant_bar = 0
        self.height_c = height_c
        self.unit = None
        self.unit_rect = None
        self.bar_width = None
        self.bar_rect = None
        self.surface = None
        self.name_surface = None
        self.name_list = None
        self.move_health = 0
        self.move_speed = 0
        self.at_dict = Atlas.load("./data/img/behaviors/HeroHMBar", "HeroHMBar")

    def start(self):
        self.unit = self.manager.unit
        self.unit_rect = self.unit.c_rect
        self.bar_width = self.unit_rect.width * self.width
        self.bar_rect = pygame.Rect(self.unit_rect.width * (1 - self.width) / 2, -15 + self.height_c, self.bar_width, 26)
        self.surface = pygame.Surface((self.bar_width, 26)).convert()
        self.surface.set_colorkey((0, 0, 0))
        self.name_surface = Font(self.name, 15, pygame.Rect(self.name_c, -35, 100, 15))
        self.name_list = self.name_surface.get_surface()[0]
        self.name_list[1].top += self.height_c
        self.manager.unit.add_surface(self.name_list[0], self.name_list[1], "hero_name")
        self.manager.unit.add_surface(self.surface, self.bar_rect, "HMBar")
        self.move_speed = self.unit.attribute_manager.attribute_dict["max_health"] / 90

    def add_level(self):
        print("waring: two HMBar were added (1 needed).")

    def update_60(self):
        health_rate = self.unit.attribute_manager.health / self.unit.attribute_manager.attribute_dict["max_health"]
        if self.unit.wait_to_death is False:
            health_color = 35, 200, 55

            self.surface.fill((0, 0, 0))
            square_rect = pygame.Rect(0, 0, self.bar_width, 9)
            pygame.draw.rect(self.surface, (80, 110, 135), square_rect, 0)

            square_rect.width = self.bar_width * health_rate
            pygame.draw.rect(self.surface, health_color, square_rect, 0)

            c_health = abs(self.unit.attribute_manager.health - self.move_health)
            self.move_speed = self.unit.attribute_manager.attribute_dict["max_health"] / 90
            if c_health > self.move_speed:
                if self.move_health > self.unit.attribute_manager.health:
                    square_rect.width = c_health / self.unit.attribute_manager.attribute_dict["max_health"] * \
                                        self.bar_width
                    square_rect.left = self.bar_width * health_rate
                    pygame.draw.rect(self.surface, (220, 65, 60), square_rect, 0)
                    self.move_health -= self.move_speed
                else:
                    square_rect.width = c_health / self.unit.attribute_manager.attribute_dict["max_health"] * \
                                        self.bar_width
                    square_rect.left = self.bar_width * health_rate - square_rect.width
                    pygame.draw.rect(self.surface, (225, 255, 225), square_rect, 0)
                    self.move_health += self.move_speed
            else:
                self.move_health = self.unit.attribute_manager.health

            if self.unit.attribute_manager.attribute_dict["max_health"] > 800:
                line_color = 212, 168, 106
                line_mode = 400
            else:
                line_color = 155, 200, 155
                line_mode = 50

            if self.cell_amount == "auto":
                line_amount = int(self.unit.attribute_manager.attribute_dict["max_health"] / line_mode) - 1
            else:
                line_amount = int(self.cell_amount) - 1

            for i in range(line_amount):
                left = (self.bar_width / (line_amount + 1) * line_amount) / line_amount * (i + 1)
                pygame.draw.line(self.surface, line_color, (left, 0), (left, 9))

            if self.unit.attribute_manager.attribute_dict["max_magic"] >= 0:
                if self.unit.attribute_manager.attribute_dict["max_magic"] > 0:
                    magic_rate = self.unit.attribute_manager.magic / \
                                 self.unit.attribute_manager.attribute_dict["max_magic"]
                else:
                    magic_rate = 0
                square_rect.left = 0
                square_rect.top = 9
                square_rect.height = 4
                square_rect.width = self.bar_width
                pygame.draw.rect(self.surface, (100, 115, 100), square_rect, 0)

                square_rect.width = self.bar_width * magic_rate
                pygame.draw.rect(self.surface, (200, 85, 200), square_rect, 0)

            pygame.draw.line(self.surface, (241, 214, 176), (0, 0), (self.bar_width, 0))
            pygame.draw.line(self.surface, (184, 137, 71), (0, 13), (self.bar_width, 13))

            self.surface.blit(self.at_dict["normal"][0][0], pygame.Rect(0, 0, 5, 13))
            self.surface.blit(self.at_dict["normal"][0][1], pygame.Rect(self.bar_width - 5, 0, 5, 13))

            self.unit.replace_surface(self.surface, self.bar_rect, "HMBar")
        else:
            self.surface.fill((0, 0, 0))
            self.unit.replace_surface(self.surface, self.bar_rect, "HMBar")

        if self.chant_bar > 0:
            square_rect = pygame.Rect(0, 18, self.bar_width * self.chant_bar, 3)
            pygame.draw.rect(self.surface, (200, 200, 200), square_rect, 0)

    def clear(self):
        self.unit.remove_surface("hero_name")
        self.unit.remove_surface("HMBar")
        super().clear()
        self.unit = None
        self.unit_rect = None
