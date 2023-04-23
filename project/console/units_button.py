from console.console_button import ConsoleButton
from display.atlas import Atlas
from auxiliary_tools.message_manager import MessageManager
import pygame


class UnitButton(ConsoleButton):
    def __init__(self, c_xy, unit):
        self.unit = unit
        self.icon = Atlas.load("./data/img/units_icon", unit.unit_panel["unit_icon"])["defeat"][0][0]
        super().__init__(c_xy=c_xy, img_source="./data/img/units_icon", img=unit.unit_panel["unit_icon"], size=(50, 50),
                         frame="UnitsFrame")
        self.if_clear = False
        self.frame = "UnitsFrame"

    def update(self):
        super().update()
        if self.unit is not None:
            surface = pygame.Surface((50, 50))
            surface.blit(self.icon, (0, 0))
            surface.set_colorkey((0, 0, 0))

            health = self.unit.attribute_manager.health
            max_health = self.unit.attribute_manager.attribute_dict["max_health"]
            magic = self.unit.attribute_manager.magic
            max_magic = self.unit.attribute_manager.attribute_dict["max_magic"]
            if health > 0:
                health_length = int(health / max_health * 50)
            else:
                health_length = 0
            if magic > 0:
                magic_length = int(magic / max_magic * 50)
            else:
                magic_length = 0

            color_rate = 1 - health_length / 50
            background_color = (0, 0, 0)
            if self.frame == "UnitsFrame":
                background_color = (160, 130 - 40 * color_rate, 110 - 20 * color_rate)
            elif self.frame == "UnitsFrameH":
                background_color = (150 + 60 * color_rate, 90 - 30 * color_rate, 90 - 30 * color_rate)
            self.surface.fill(background_color)

            pygame.draw.rect(surface, color=(100, 80, 70), rect=pygame.Rect(0, 42, 50, 5))
            pygame.draw.rect(surface, color=(70, 200, 70), rect=pygame.Rect(0, 42, health_length, 5))
            if max_magic > 0:
                pygame.draw.rect(surface, color=(120, 100, 90), rect=pygame.Rect(0, 39, 50, 3))
                pygame.draw.rect(surface, color=(200, 70, 200), rect=pygame.Rect(0, 39, magic_length, 3))

            self.change_surface(surface, self.frame)

            if self.mouse_on:
                cursor = "chooseDefeat"
                if self.unit.flag.contain_flag("own"):
                    cursor = "chooseOWN"
                elif self.unit.flag.contain_flag("enemy"):
                    cursor = "chooseENEMY"
                MessageManager.send_message("cursor_play", cursor)

            if self.unit.wait_to_death:
                self.unit = None
        else:
            surface = pygame.Surface((50, 50))
            surface.set_colorkey((0, 0, 0))
            self.change_surface(surface, "NoFrame")

    def set_high_light(self, flag):
        if self.unit is not None:
            if self.unit.flag.contain_flag(flag, must_have_all=True):
                self.frame = "UnitsFrameH"
            else:
                self.frame = "UnitsFrame"

    def mouse_down(self):
        if self.unit is not None:
            MessageManager.send_message("choose_units", [self.unit])

    def clear(self):
        super().clear()
        self.unit = None
