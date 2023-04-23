from unit_tools.skill import Skill
from units.effect.add_behavior import AddBehavior
from units.behaviors.speed_up_test import SpeedUp
from units.instructions.effect_self import EffectSelfAdditional


class SpeedUpSkill(Skill):
    def __init__(self, unit):
        effect = AddBehavior(behavior=SpeedUp())
        super().__init__(target_mode=None, unit=unit, effect=effect, cooling=10, magic_require=5, quick_spell=True)
        self.flag.add_flag("speed_up_test")

    def instruction(self, data):
        return EffectSelfAdditional(self)
