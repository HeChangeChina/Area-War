from unit_tools.skill import Skill
from auxiliary_tools.tech_tree import TechTree


class TechUnlockEffect(Skill):
    def __init__(self, unit, tech, effect=None):
        super().__init__(unit, None)
        self.flag.add_flag(tech)
        self.tech = tech
        self.unlock = False
        self.effect = effect

    def update(self):
        super().update()
        self.enabled = self.unlock
        if self.unlock is False and TechTree.have_tech(self.unit.team, self.tech):
            if self.effect is not None:
                self.effect.take_effect(self.unit, self.unit)
            self.unlock = True
