from unit_tools.behavior import Behavior
from display.font import FontSurface
from pygame import Rect
from pygame import Surface
from pygame import draw
from math import pi


class ProduceListShower(Behavior):
    def __init__(self, height_c=0):
        super().__init__()
        self.flag.add_flag(["ProduceListShower", "info_show"])
        self.c_rect = None
        self.surface = None
        self.height_c = height_c

    def start(self):
        unit_rect = self.unit.c_rect
        self.surface = Surface((50, 50))
        self.surface.set_colorkey((0, 0, 0))
        self.c_rect = Rect(unit_rect.width / 2 - 25, -40 + self.height_c, 50, 50)
        self.unit.add_surface(self.surface, self.c_rect, "ProduceListShower")

    def update_60(self):
        self.surface.fill((0, 0, 0))
        production_list = self.unit.attribute_manager.get_attribute("production_list")
        if production_list is not None and production_list[0] is not None:
            angle = 2 * pi * self.unit.attribute_manager.get_attribute("production_bar")[0]
            draw_rect = Rect(0, 0, 50, 50)
            draw.arc(self.surface, (100, 100, 100), draw_rect, 0, pi * 2, 4)
            draw.arc(self.surface, (165, 200, 235), draw_rect, pi / 2, angle + pi / 2, 4)

            production_count = 0
            while production_list[production_count] is not None:
                production_count += 1
                if production_count >= 7:
                    break

            text_surface = FontSurface(text=str(production_count), color=(100, 100, 100), size=25).surface
            text_pos = 25 - text_surface.get_width() / 2, 25 - text_surface.get_height() / 2
            self.surface.blit(text_surface, text_pos)

    def clear(self):
        self.unit.remove_surface("ProduceListShower")
        super().clear()

