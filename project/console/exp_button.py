from console.console_button import ConsoleButton
from display.atlas import Atlas
from display.font import FontSurface
import pygame


class ExpButton(ConsoleButton):
    def __init__(self, c_xy, unit=None):
        super().__init__(c_xy, size=(400, 50), frame="expFrame", text_shift=170)
        self.unit = unit
        self.unit_exp = -100
        self.unit_level = -1
        self.frame = Atlas.load("./data/img/console", "expFrame")["defeat"][0][0]
        self.set_unit(unit)

    def update(self):
        super().update()
        if self.unit is not None:
            if self.unit_exp != self.unit.attribute_manager.exp or self.unit_level != self.unit.attribute_manager.level:
                self.update_text(self.unit)
                self.unit_level = self.unit.attribute_manager.level
                self.unit_exp = self.unit.attribute_manager.exp

    def update_text(self, unit):
        if unit is not None:
            exp_now = unit.attribute_manager.exp
            exp_total = unit.attribute_manager.get_now_exp_level()
            exp_rate = exp_now / exp_total if exp_now != 0 else 0
            # 160 120 90
            surface = pygame.Surface((400, 50))
            surface.fill((160, 120, 90))
            surface.set_colorkey((0, 0, 0))

            pygame.draw.rect(surface, (120, 100, 160), pygame.Rect(50, 0, 350 * exp_rate, 50))
            pygame.draw.rect(surface, (200, 180, 230), pygame.Rect(50, 10, 350 * exp_rate, 6))
            pygame.draw.rect(surface, (80, 90, 110), pygame.Rect(50, 36, 350 * exp_rate, 10))
            surface.blit(self.frame, (0, 0))

            text = "等级" + str(unit.attribute_manager.level) + "-" + unit.unit_panel["title"]
            text_surface = FontSurface(text, 16, color=(240, 225, 255)).surface
            surface.blit(text_surface, (200 - text_surface.get_width() / 2, 16))

            topic = str(unit.attribute_manager.level)
            topic_surface = FontSurface(topic, 30, color=(110, 100, 90)).surface
            surface.blit(topic_surface, ((30 - topic_surface.get_width() / 2), 10))

            self.change_surface(surface, None)
            self.change_text(str(int(exp_now)) + "/" + str(exp_total))

    def set_unit(self, unit):
        self.unit = unit
        if unit is not None:
            self.update_text(unit)
            self.unit_level = unit.attribute_manager.level
            self.unit_exp = unit.attribute_manager.exp

    def clear(self):
        self.unit = None
        super().clear()
