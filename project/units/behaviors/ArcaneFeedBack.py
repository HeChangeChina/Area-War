from unit_tools.behavior import Behavior


class ArcaneFeedBack(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("arcane_feed_back")
        self.icon = "ArcaneFeedBackIS"
        self.level = 1

    def start(self):
        self.icon_visible = True
        self.last_frame = 360
        self.add_attribute_revise("harm_cause_rate", 0.1, "arcane_feed_back")
        self.name = "魔力回馈"
        self.describe = "造成的伤害提升"
        self.polarity = "positive"
        self.add_animation("ArcaneFeedBack", "ArcaneFeedBack")

    def add_level(self):
        self.last_frame = 360
        self.level += 1 if self.level < 3 else 0
        self.set_attribute_revise("arcane_feed_back", 0.1 * self.level)

    def clear(self):
        super().clear()
