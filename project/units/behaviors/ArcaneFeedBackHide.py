from unit_tools.behavior import Behavior


class ArcaneFeedBackHide(Behavior):
    def __init__(self, skill):
        super().__init__()
        self.flag.add_flag("arcane_feed_back_hide")
        self.enabled = False
        self.icon_visible = False
        self.skill = skill
        self.magic_used = 0

    def magic_use(self, value):
        if self.enabled:
            self.magic_used += value
            while self.magic_used >= 30:
                self.magic_used -= 30
                self.skill.add_arcane_behavior()

    def clear(self):
        super().clear()
        self.skill = None
