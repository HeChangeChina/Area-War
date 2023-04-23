from unit_tools.skill import Skill
from units.instructions.flash import Flash
from unit_tools.effect import Effect
from unit_tools.filter import NullFilter


class SkillFlash(Skill):
    def __init__(self, unit, magic_require=15, cooling=3, length=360, effect=Effect(),
                 tech_require=None, tech_mode="have"):
        super().__init__(unit, target_mode=NullFilter(True), effect=effect, magic_require=magic_require,
                         cooling=cooling, tech_require=tech_require, tech_mode=tech_mode)
        self.flag.add_flag("flash")
        self.magic_require = magic_require
        self.cooling = cooling
        self.length = length

    def instruction(self, data):
        return Flash(self, data[0], self.length)