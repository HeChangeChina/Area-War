from unit_tools.behavior import Behavior


class SpeedUp(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("speed_up_test")

    def start(self):
        self.icon_visible = True
        self.last_frame = 300
        self.add_attribute_revise("speed_rate", 3.5, "speed")
        self.add_attribute_revise("weapon_speed", 3, "weapon_speed")
        self.name = "疾跑"
        self.describe = "小幅度提高该单位的速度"
        self.polarity = "positive"
