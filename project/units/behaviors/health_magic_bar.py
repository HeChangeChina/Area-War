from unit_tools.behavior import Behavior
import pygame


class HMBar(Behavior):
    def __init__(self, width=1, cell_amount="auto", height_c=0):
        super().__init__()
        self.flag.add_flag(["HMBar", "info_show"])
        self.width = width
        self.cell_amount = cell_amount
        self.height_c = height_c
        self.chant_bar = 0
        self.chant_bar_color = 200, 200, 200
        self.unit = None
        self.unit_rect = None
        self.bar_width = None
        self.bar_rect = None
        self.surface = None
        # self.at_dict = Atlas.load("./data/img/behaviors/HMBar", "hmbframe")

    def start(self):
        self.unit = self.manager.unit
        self.unit_rect = self.unit.c_rect
        self.bar_width = self.unit_rect.width * self.width
        self.bar_rect = pygame.Rect(self.unit_rect.width * (1 - self.width) / 2, -15 + self.height_c, self.bar_width, 20)
        self.surface = pygame.Surface((self.bar_width, 20)).convert()
        self.surface.set_colorkey((0, 0, 0))
        self.manager.unit.add_surface(self.surface, self.bar_rect, "HMBar")

    def add_level(self):
        print("waring: two HMBar were added (1 needed).")

    def update_60(self):
        health_rate = self.unit.attribute_manager.health / self.unit.attribute_manager.attribute_dict["max_health"]
        if health_rate < 1 or self.unit.attribute_manager.magic != self.unit.attribute_manager.attribute_dict["max_magic"]:
            if health_rate < 0.75:
                color_rate = self.unit.attribute_manager.health / \
                             (self.unit.attribute_manager.attribute_dict["max_health"] * 0.75)
            else:
                color_rate = 1
            health_color = int(220 + (50 - 220) * color_rate), int(50 + (220 - 50) * color_rate), \
                           int(45 + (70 - 45 * color_rate))

            self.surface.fill((0, 0, 0))
            square_rect = pygame.Rect(0, 0, self.bar_width, 7)
            pygame.draw.rect(self.surface, (80, 110, 135), square_rect, 0)

            square_rect.width = self.bar_width * health_rate
            pygame.draw.rect(self.surface, health_color, square_rect, 0)

            square_rect.width = self.bar_width
            pygame.draw.rect(self.surface, (212, 168, 106), square_rect, 1)

            if self.unit.attribute_manager.attribute_dict["max_health"] > 800:
                line_color = 212, 168, 106
                line_mode = 400
            else:
                line_color = 0, 0, 0
                line_mode = 50

            if self.cell_amount == "auto":
                line_amount = int(self.unit.attribute_manager.attribute_dict["max_health"] / line_mode) - 1
            else:
                line_amount = int(self.cell_amount) - 1

            for i in range(line_amount):
                left = (self.bar_width / (line_amount + 1) * line_amount) / line_amount * (i + 1)
                pygame.draw.line(self.surface, line_color, (left, 1), (left, 5))

            if self.unit.attribute_manager.attribute_dict["max_magic"] > 0:
                magic_rate = self.unit.attribute_manager.magic / self.unit.attribute_manager.attribute_dict["max_magic"]
                square_rect.top = 8
                square_rect.height = 4
                square_rect.width = self.bar_width
                pygame.draw.rect(self.surface, (100, 115, 100), square_rect, 0)

                square_rect.width = self.bar_width * magic_rate
                pygame.draw.rect(self.surface, (200, 85, 200), square_rect, 0)

            # self.surface.blit(self.at_dict["normal"][0][0], pygame.Rect(0, 0, 5, 7))
            # self.surface.blit(self.at_dict["normal"][0][1], pygame.Rect(self.bar_width - 5, 0, 5, 7))

            self.unit.replace_surface(self.surface, self.bar_rect, "HMBar")
        else:
            self.surface.fill((0, 0, 0))
            self.unit.replace_surface(self.surface, self.bar_rect, "HMBar")

        if self.chant_bar > 0:
            square_rect = pygame.Rect(0, 14, self.bar_width * self.chant_bar, 3)
            pygame.draw.rect(self.surface, self.chant_bar_color, square_rect, 0)

    def clear(self):
        if self.unit is not None:
            self.unit.remove_surface("HMBar")
            self.unit = None
            self.unit_rect = None
        super().clear()
