from unit_tools.skill import Skill
from unit_tools.effect import Effect
from units.instructions.approach_and_use import ApproachAndUse


class SelfChantSkill(Skill):
    def __init__(self, unit, quick_spell=True, cooling=0, effect=Effect(),
                 animate="skill", can_auto_use=False, magic_require=0, chant_time=1,
                 chant_animate="chant", skill_animate="skill", animate_advance_frame=15,
                 flag="chant_skill", chant_stoppable=False, target_y=None, pre_effect=None,
                 tech_require=None, tech_mode="have"):
        self.chant_frame = chant_time * 60
        self.chant_animate = chant_animate
        self.skill_animate = skill_animate
        self.animate_advance = animate_advance_frame
        self.chant_stoppable = chant_stoppable
        self.target_y = target_y
        self.pre_effect = pre_effect

        super().__init__(unit, None, quick_spell, cooling, effect, animate, can_auto_use, magic_require,
                         tech_require=tech_require, tech_mode=tech_mode)
        self.flag.add_flag(flag)
        self.flag.add_flag("instruction_replace")

    def instruction(self, data):
        return ApproachAndUse(self, self.unit, self.chant_frame, self.chant_animate, self.animate_advance,
                              self.skill_animate, 1000, 1000, self.chant_stoppable, self.pre_effect)

    def update(self):
        super().update()
