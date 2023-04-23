from unit_tools.behavior import Behavior


class FaithBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("faith_behavior")

    def start(self):
        self.icon_visible = False
        self.add_attribute_revise("max_magic", 50, "faith_behavior")
