from units.instructions.hold import Hold
from unit_tools.skill import Skill


class SkillHold(Skill):
    def __init__(self, unit):
        super().__init__(unit, None)
        self.flag.add_flag("hold")

    def get_instruction(self, data):
        return Hold(self, self.unit.weapons)
