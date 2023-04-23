from units.skills.chant_skill import ChantSkill
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.mixed_effect import MixedEffect
from units.effect.hurt import Hurt
from units.effect.create_bullet import CreateBullet
from units.effect.search_range import SearchRange
from units.sight.follow_sight import FollowSight
from auxiliary_tools.bullet_pre import BulletPre
from unit_tools.filter import Filter


class FireballSkill(ChantSkill):
    def __init__(self, unit):
        hurt_effect_50 = Hurt(value=140, hurt_type=1)
        hurt_effect_25 = Hurt(value=70, hurt_type=1)
        search_range = SearchRange(effect=hurt_effect_25, range=50, target_included=False, required_flag=["enemy"],
                                   excluded_flag=["building"])
        range_mixed_effect = MixedEffect(effects=(hurt_effect_50, (search_range, "fire_spread")))
        create_explosion = CreateSpecialEffect(effect_name="FireBlastMIDDLE", size=(80, 80), fps_level=1)
        bullet = BulletPre(name="fireballMIDDLE", effect=range_mixed_effect, direct=True,
                           trajectory_name="fireballSMALLT",
                           trajectory_size=(20, 20), trajectory_fps=0, hit_effect=create_explosion)
        create_bullet = CreateBullet(bullet=bullet)
        fireball_filter = Filter(unit, ["unit", "enemy"], ["building"])
        super().__init__(unit, fireball_filter, can_auto_use=True, cooling=7, magic_require=60,
                         effect=create_bullet, flag="fireball", quick_spell=False,
                         sight=FollowSight("sight100C", 2, coll_range=50), chant_animate="attack",
                         skill_animate="attack", aiming_range=600, chant_time=1.5)

    def get_target(self):
        for i in self.unit.radar_list:
            if self.target_mode.filter(i) and \
                    i.attribute_manager.health < i.attribute_manager.get_attribute("max_health") - 15:
                return i
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
