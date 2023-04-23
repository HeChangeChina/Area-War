from unit_tools.skill import Skill
from unit_tools.effect import Effect
from units.instructions.approach_and_use import ApproachAndUse


class ChantSkill(Skill):
    def __init__(self, unit, target_mode, quick_spell=True, cooling=0, effect=Effect(),
                 animate="skill", can_auto_use=False, magic_require=0, sight=None, chant_time=1,
                 chant_animate="chant", skill_animate="skill", animate_advance_frame=15,
                 aiming_range=400, escape_range=500, flag="chant_skill", chant_stoppable=False,
                 target_y=None, pre_effect=None, tech_require=None, tech_mode="have"):
        self.chant_frame = chant_time * 60
        self.chant_animate = chant_animate
        self.skill_animate = skill_animate
        self.animate_advance = animate_advance_frame
        self.aiming_range = aiming_range
        self.escape_range = escape_range
        self.chant_stoppable = chant_stoppable
        self.target_y = target_y
        self.pre_effect = pre_effect

        super().__init__(unit, target_mode, quick_spell, cooling, effect, animate, can_auto_use, magic_require, sight,
                         tech_require=tech_require, tech_mode=tech_mode)
        self.flag.add_flag(flag)
        self.flag.add_flag("instruction_replace")

    def take_effect(self):
        return super().take_effect()

    def instruction(self, data):
        if self.target_y is not None and (type(data) is list or type(data) is tuple):
            data = (data[0], self.target_y)
        return ApproachAndUse(self, data, self.chant_frame, self.chant_animate, self.animate_advance,
                              self.skill_animate, self.aiming_range, self.escape_range, self.chant_stoppable,
                              self.pre_effect)
