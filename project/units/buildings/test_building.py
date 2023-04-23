from units.building import Building
from units.effect.create_bullet import CreateBullet
from units.effect.hurt import Hurt
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.mixed_effect import MixedEffect
from units.effect.search_range import SearchRange
from units.skills.produce import ProduceSkill
from units.skills.chant_skill import ChantSkill
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.produce_lists_shower import ProduceListShower
from unit_tools.attribute_manager import AttributeManager
from unit_tools.filter import Filter
from unit_tools.weapon import Weapon
from units.sight.follow_sight import FollowSight
from auxiliary_tools.bullet_pre import BulletPre
import pygame


class TestBuilding(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/TestBuilding", "TestBuilding", pygame.Rect(x, y, 300, 200),
                         unit_height_c=196,
                         attribute_manager=AttributeManager(max_health=800, max_magic=100, magic_armor=100,
                                                            armor_tech=("slim", "slim"), physical_armor=5),
                         population_produce=3000)
        self.flag.add_flag(["test_building", "production_unit"])
        self.volume = 80
        self.cost = {"gold": 300, "wood": 160}

        self.behavior_manager.add(HMBar(width=0.8, height_c=50))
        self.behavior_manager.add(ProduceListShower())

        hurt_effect_5 = Hurt(value=5, hurt_type=1)
        create_explosion = CreateSpecialEffect(effect_name="arcaneBlastNORMAL", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="arcaneNORMAL", effect=hurt_effect_5, direct=False, trajectory_name="arcaneT",
                           trajectory_size=(20, 20), trajectory_fps=1, hit_effect=create_explosion)
        create_bullet = CreateBullet(bullet=bullet)
        search_range = SearchRange(effect=create_bullet, max_amount=4, range=100, required_flag=["unit", "enemy"],
                                   excluded_flag=["building"])
        weapon_filter = Filter(self, ["unit", "enemy"], ["building"])
        weapon = Weapon(weapon_filter, tech="slim", effect=search_range, aim_range=400, base_hurt=5, name="奥术冲击",
                        hurt_describe="魔法伤害", describe="其实是里面的魔法师发射的。", interval=0.5, fire_animate="defeat",
                        aiming_animate="defeat")
        self.weapons.add(weapon)

        hurt_effect_50 = Hurt(value=50, hurt_type=1)
        hurt_effect_25 = Hurt(value=25, hurt_type=1)
        search_range = SearchRange(effect=hurt_effect_25, range=300, target_included=False, required_flag=["enemy"])
        range_mixed_effect = MixedEffect(effects=(hurt_effect_50, search_range))
        create_explosion = CreateSpecialEffect(effect_name="FireBlastMIDDLE", size=(80, 80), fps_level=1)
        bullet = BulletPre(name="fireballSMALL", effect=range_mixed_effect, direct=True,
                           trajectory_name="fireballSMALLT",
                           trajectory_size=(30, 30), trajectory_fps=0, hit_effect=create_explosion)
        create_bullet = CreateBullet(bullet=bullet)
        fireball_filter = Filter(self, ("unit", "enemy"))

        fireball_skill = ChantSkill(self, fireball_filter, can_auto_use=True, cooling=6, magic_require=0,
                                    effect=create_bullet, flag="fireball", quick_spell=False,
                                    sight=FollowSight("sight100C", 2, coll_range=300), chant_animate="defeat",
                                    skill_animate="defeat", aiming_range=1000)
        self.skill_manager.add(fireball_skill)
        self.skill_panel.replace("skill", fireball_skill, describe="火球术",
                                 key="T", line=3, column=1, mouse=False)

        cost = {"gold": 80}
        skill_produce = ProduceSkill(self, "worker", "workerIcon", cost, 1, 3)
        self.skill_manager.add(skill_produce)
        self.skill_panel.replace("skill", skill_produce, describe="生产-史莱姆&制造一个史莱姆",
                                 key="F", line=3, column=0, mouse=False)

        self.unit_panel["unit_label"] = ("建筑", "大型单位")
        self.unit_panel["armor_name"] = ("城墙", "城墙")
        self.unit_panel["name"] = "测试建筑"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "普通的建筑"

        self.base_bullet_anchor = [0, 15]
