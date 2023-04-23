from unit_tools.behavior import Behavior


class RoarBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("arcane_light")
        self.icon = "roarIconS"

    def start(self):
        self.icon_visible = True
        self.last_frame = 1200
        self.add_attribute_revise("harm_cause_rate", 0.25, "roar")
        self.name = "战吼"
        self.describe = "该单位造成的伤害提升"
        self.polarity = "positive"
