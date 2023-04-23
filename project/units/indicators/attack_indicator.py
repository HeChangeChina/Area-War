from units.indicator import Indicator
from units.visible_effect.move_indicator_effect import MoveIndicatorEffect


class AttackIndicator(Indicator):
    def __init__(self, x):
        self.x = x - 25
        super().__init__()

    def get_effect(self):
        return [MoveIndicatorEffect(self.x, img="attackEffect"), 10, 1]
