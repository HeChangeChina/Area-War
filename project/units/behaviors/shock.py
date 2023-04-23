from unit_tools.behavior import Behavior


class ShockBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("arcane_light")
        self.icon = "shockIS"

    def start(self):
        self.icon_visible = True
        self.last_frame = 480
        self.add_attribute_revise("weapon_speed", -0.5, "weapon_speed")
        self.add_attribute_revise("speed_rate", -0.5, "speed")
        self.name = "震撼"
        self.describe = "该单位的移动速度与武器速度被降低了"
        self.polarity = "negative"
