from unit_tools.behavior import Behavior
from units.effect.hurt import Hurt


class Poisoning(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("poisoning")
        self.icon = "envenomedIconS"
        self.level = 1
        self.hurt_effect = None

    def start(self):
        self.icon_visible = True
        self.last_frame = 420
        self.add_attribute_revise("physical_armor", -2, "poisoning")
        self.name = "中毒"
        self.describe = "该单位的物理护甲降低，受到持续伤害"
        self.polarity = "negative"
        self.add_animation("poisoning", "poisoning")
        self.hurt_effect = Hurt(value=2 / 15, hurt_type=2, have_event=False)

    def add_level(self):
        self.last_frame = 420
        self.level += 1 if self.level < 3 else 0
        self.set_attribute_revise("physical_armor", -2 * self.level)

    def update_15(self):
        self.hurt_effect.data["value"] = self.level * 2 / 15
        self.hurt_effect.take_effect(self.unit, self.unit)

    def clear(self):
        super().clear()
