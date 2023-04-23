from units.skills.chant_skill import ChantSkill
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.mixed_effect import MixedEffect
from units.effect.heal import Heal
from unit_tools.filter import Filter


class HealSkill(ChantSkill):
    def __init__(self, unit):
        heal_effect = Heal(value=35)
        create_explosion = CreateSpecialEffect(effect_name="heal", size=(70, 80), fps_level=1)
        heal_mixed_effect = MixedEffect(effects=[heal_effect, create_explosion])
        heal_filter = Filter(unit, ["unit", "human"], ["enemy"])
        super().__init__(unit, heal_filter, cooling=2.5, magic_require=10,
                        effect=heal_mixed_effect, flag="heal", quick_spell=False, chant_time=0.4,
                        chant_animate="attack", skill_animate="attack", aiming_range=500,
                        animate_advance_frame=10, can_auto_use=True)

    def get_target(self):
        for i in self.unit.radar_list:
            if self.target_mode.filter(i) and i.team == self.unit.team and\
                    i.attribute_manager.health < i.attribute_manager.get_attribute("max_health") - 15:
                return i
        if self.unit.attribute_manager.health < self.unit.attribute_manager.get_attribute("max_health") - 15:
            return self.unit
        return None

    def auto_use_judge(self):
        if self.unit.instructor.waiting:
            target = self.get_target()
            if target is None:
                return False
            else:
                return target, "clear"
        elif self.unit.instructor.now_instruction is not None and\
                self.unit.instructor.now_instruction.flag.contain_flag("stoppable"):
            target = self.get_target()
            if target is not None:
                instruction = self.instruction(target)
                self.unit.instructor.insert_instruction(instruction)
        return False
