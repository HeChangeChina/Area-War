from unit_tools.attribute_manager import AttributeManager
from units.movable_unit import MovableUnit
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.skills.speed_up_test import SpeedUpSkill
from units.skills.chant_skill import ChantSkill
from units.skills.build import BuildSkill
from units.skills.repair import RepairSkill
from units.effect.create_bullet import CreateBullet
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.mixed_effect import MixedEffect
from units.effect.search_range import SearchRange
from units.effect.hurt import Hurt
from units.sight.follow_sight import FollowSight
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
from auxiliary_tools.bullet_pre import BulletPre
import pygame


class Slim(MovableUnit):
    def __init__(self, x, y):
        super().__init__("./data/img/units/movable/slim", "slim", pygame.Rect(x, y, 50, 50), unit_height_c=32,
                         attribute_manager=AttributeManager(0, max_health=240, max_magic=20, magic_armor=20,
                                                            armor_tech=("slim", "slim")), population_cost=1)
        self.flag.add_flag(["slim", "land_force"])

        hurt_effect_15 = Hurt(value=18, hurt_type=0)
        weapon_filter = Filter(self, ["unit", "enemy", "land_force"], ["air_force"])
        weapon = Weapon(weapon_filter, tech="slim", effect=hurt_effect_15, aim_range=10, escape_range=50, base_hurt=18,
                        name="撞击", hurt_describe="物理伤害", describe="史莱姆喜欢撞向自己的敌人")
        self.weapons.add(weapon)

        self.behavior_manager.add(HMBar())
        self.behavior_manager.add(Shadow(c_x=0))
        # self.behavior_manager.add(HMBar(width=0.75))

        hurt_effect_50 = Hurt(value=50, hurt_type=1)
        hurt_effect_25 = Hurt(value=25, hurt_type=1)
        search_range = SearchRange(effect=hurt_effect_25, range=300, target_included=False, required_flag=["enemy"])
        range_mixed_effect = MixedEffect(effects=(hurt_effect_50, search_range))
        create_explosion = CreateSpecialEffect(effect_name="FireBlastMIDDLE", size=(80, 80), fps_level=1)
        bullet = BulletPre(name="fireballSMALL", effect=range_mixed_effect, direct=True, trajectory_name="fireballSMALLT",
                           trajectory_size=(30, 30), trajectory_fps=0, hit_effect=create_explosion)
        create_bullet = CreateBullet(bullet=bullet)
        fireball_filter = Filter(self, ["unit", "enemy"])

        fireball_skill = ChantSkill(self, fireball_filter, can_auto_use=True, cooling=6, magic_require=15,
                                    effect=create_bullet, flag="fireball", quick_spell=False,
                                    sight=FollowSight("sight100C", 2, coll_range=300))

        build_skill = BuildSkill(self, "TestBuilding", 196, 300, 0, dict())
        speed_up = SpeedUpSkill(self)
        repair_skill = RepairSkill(self)

        self.skill_manager.add(speed_up)
        self.skill_manager.add(fireball_skill)
        self.skill_manager.add(build_skill)
        self.skill_manager.add(repair_skill)

        self.skill_panel.replace("skill", speed_up, describe="疾跑&小幅度提升移动速度",
                                 key="F", line=3, column=0, mouse=True, panel="skills")
        self.skill_panel.replace("skill", fireball_skill, describe="火球术&对目标敌人造成50点魔法伤害，并对周围的所有单位造成25点魔法伤害",
                                 key="T", line=3, column=1, mouse=True, panel="skills")
        self.skill_panel.replace("skill", build_skill, describe="建造",
                                 key="B", line=3, column=0, mouse=True, panel="defeat")
        self.skill_panel.replace("skill", describe="打开技能面板&史莱姆为什么会有这些技能呢?",
                                 line=3, column=4, panel_to="skills", skill=None, key="F")
        self.skill_panel.replace("skill", describe="返回",
                                 line=3, column=4, panel_to="defeat", skill=None, key="A", panel="skills")
        self.skill_panel.replace("skill", describe="维修&消耗资源，维修友方或己方机械单位或者建筑，每秒回复目标15点血量",
                                 line=3, column=1, skill=repair_skill, key="R", panel="defeat", mouse=True)

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "元素生物")
        self.unit_panel["armor_icon"] = ("MucusArmorP", "MucusArmorM")
        self.unit_panel["armor_name"] = ("粘液护甲", "元素皮肤")
        self.unit_panel["name"] = "史莱姆"
        self.unit_panel["unit_icon"] = "slimIcon"
        self.unit_panel["title"] = "随处可见的史莱姆"

        self.attribute_manager.exp_level = (300, 400, 500, 600)

        self.exp_produce = 5

    def update_60_m(self):
        pass
