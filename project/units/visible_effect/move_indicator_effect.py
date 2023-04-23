from display.normal_display import NormalDisplay
from auxiliary_tools.exact_rect import ERect


class MoveIndicatorEffect(NormalDisplay):
    def __init__(self, x, img="move"):
        self.rect = ERect(x - 15, 750, 80, 80)
        super().__init__("./data/img/effect/move", img, self.rect.rect())
        self.time = 0
        self.flag.add_flag("move")
        self.update()

    def update(self):
        if self.time <= 30:
            self.rect.top = 690 + 3.5 * self.time
            self.rect.left += 1.2
            self.c_rect.top = self.rect.top
            self.c_rect.left = self.rect.left

            self.shader.set_size((1 - (self.time * 0.03)), (1 - (self.time * 0.03)))

            self.time += 1
        else:
            self.if_clear = True
