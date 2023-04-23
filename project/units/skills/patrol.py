from units.instructions.patrol import Patrol
from unit_tools.skill import Skill
from unit_tools.filter import NullFilter


class SkillPatrol(Skill):
    def __init__(self, unit):
        super().__init__(unit, target_mode=NullFilter(True))
        self.flag.add_flag("patrol")

    def get_instruction(self, data):
        return Patrol(self, self.unit.weapons, data[0])
