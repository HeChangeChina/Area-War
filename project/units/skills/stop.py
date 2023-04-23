from unit_tools.skill import Skill
from units.instructions.stop import Stop


class SkillStop(Skill):
    def __init__(self, unit):
        super().__init__(unit, target_mode=None)
        self.flag.add_flag("stop")

    def instruction(self, data):
        return Stop(self)
