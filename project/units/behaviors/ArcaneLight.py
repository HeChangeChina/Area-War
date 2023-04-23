from unit_tools.behavior import Behavior


class ArcaneLightBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("arcane_light")
        self.icon = "ArcaneLightIS"

    def start(self):
        self.icon_visible = True
        self.last_frame = 10
        self.add_attribute_revise("magic_recovery_speed", 1.5, "arcane_light")
        self.name = "奥术光辉"
        self.describe = "魔法回复速度提升"
        self.polarity = "positive"

    def add_level(self):
        self.last_frame = 10
