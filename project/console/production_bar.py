from console.console_button import ConsoleButton
from pygame import Surface
from pygame import draw
from pygame import Rect


class ProductionBar(ConsoleButton):
    def __init__(self, x, y):
        super().__init__([x, y], frame="ProductionBarFrame", size=(270, 24), text_shift=60)
        self.bar_rate = -1
        self.change_rate(0.5, 10)

    def change_rate(self, rate, total_time):
        if self.bar_rate != rate:
            self.bar_rate = rate
            surface = Surface((270, 24))
            surface.fill((160, 130, 110))
            rect = Rect(0, 4, 270 * rate, 24)
            draw.rect(surface, (230, 200, 150), rect)
            rect = Rect(0, 4, 270 * rate, 4)
            draw.rect(surface, (250, 230, 200), rect)
            rect = Rect(0, 16, 270 * rate, 4)
            draw.rect(surface, (160, 140, 100), rect)
            self.change_surface(surface, "ProductionBarFrame")
            self.change_text(str(int(total_time * rate)) + "/" + str(total_time))
