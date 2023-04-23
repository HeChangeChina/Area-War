from display.font import FontSurface
from base import Base
from pygame import Rect


class ConsoleText(Base):
    def __init__(self):
        super().__init__()
        self.unit = None
        self.text = "无文本"
        self.font = FontSurface(text="无文本", size=18, color=(235, 210, 165))
        self.c_rect = Rect(0, -100, 0, 0)

    def set_unit(self, unit):
        self.unit = unit

    def update(self):
        if self.unit is not None:
            if self.text != self.unit.unit_panel["text"]:
                self.text = self.unit.unit_panel["text"]
                self.font.change_text(self.text)
                self.c_rect.left = 760 - self.font.surface.get_width() / 2
            self.c_rect.top = 910 + self.unit.unit_panel["text_y"]
            self.c_rect.width = self.font.surface.get_width()
        else:
            self.c_rect.top = -100

    def get_surface(self):
        return [self.font.surface, self.c_rect]

    def clear(self):
        self.unit = None
        super().clear()
