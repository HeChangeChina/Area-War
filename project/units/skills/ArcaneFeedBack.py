from unit_tools.skill import Skill
from units.effect.add_behavior import AddBehavior
from units.behaviors.ArcaneFeedBack import ArcaneFeedBack
from units.behaviors.ArcaneFeedBackHide import ArcaneFeedBackHide


class ArcaneFeedBackSkill(Skill):
    def __init__(self, unit, tech_require=None):
        effect = AddBehavior(behavior=ArcaneFeedBack())
        super().__init__(unit, None, tech_require=tech_require, effect=effect)
        self.flag.add_flag("arcane_feed_back")
        self.hide_behavior = ArcaneFeedBackHide(self)
        self.unit.behavior_manager.add(self.hide_behavior)

    def add_arcane_behavior(self):
        self.effect.take_effect(self.unit, self.unit)

    def update(self):
        super().update()
        self.hide_behavior.enabled = self.enabled

    def clear(self):
        self.hide_behavior.last_frame = 1
        self.hide_behavior = None
        super().clear()
