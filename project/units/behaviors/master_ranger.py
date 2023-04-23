from unit_tools.behavior import Behavior


class MasterRangerBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("master_ranger")

    def start(self):
        self.icon_visible = False
        self.add_attribute_revise("weapon_speed", 0.3, "weapon_speed")
        self.polarity = "positive"
