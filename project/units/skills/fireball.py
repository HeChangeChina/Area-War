from unit_tools.skill import Skill
from unit_tools.filter import Filter
from unit_tools.bullet import Bullet
from units.effect.create_bullet import CreateBullet
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.mixed_effect import MixedEffect
from units.effect.search_range import SearchRange
from units.effect.hurt import Hurt


# 这个技能已经由 chant_skill 实现，这里是原本的未完成版本
class Fireball(Skill):
    def __init__(self, unit, chant_time=1):
        self.chant_frame = chant_time * 60
        target_mode = Filter(["unit", "enemy"])

        hurt_effect_50 = Hurt(value=50, hurt_type=1)
        hurt_effect_25 = Hurt(value=25, hurt_type=1)
        search_range = SearchRange(effect=hurt_effect_25, range=50, target_included=False)
        range_mixed_effect = MixedEffect(effects=(hurt_effect_50, search_range))
        create_explosion = CreateSpecialEffect(effect_name="FireBlastMIDDLE", size=(80, 80), fps_level=1)
        bullet_effect = MixedEffect(effects=(range_mixed_effect, create_explosion))
        bullet = Bullet(name="fireballSMALL", effect=bullet_effect, direct=True, trajectory_name="fireballSMALLT",
                        trajectory_size=(30, 30))
        create_bullet = CreateBullet(bullet=bullet)

        super().__init__(unit=unit, target_mode=target_mode, quick_spell=False, cooling=6, magic_require=15,
                         effect=create_bullet, can_auto_use=True)

    def instruction(self, data):
        pass
