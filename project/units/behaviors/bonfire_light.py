from unit_tools.behavior import Behavior


class BonfireLight(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("bonfire_light")
        self.icon = "bonfireHALOS"

    def start(self):
        self.icon_visible = True
        self.last_frame = 10
        self.add_attribute_revise("health_recovery_speed", 1.5, "bonfire_light")
        self.name = "篝火"
        self.describe = "该单位的生命回复速度提高"
        self.polarity = "positive"

    def add_level(self):
        self.last_frame = 10
