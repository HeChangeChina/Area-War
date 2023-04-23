from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.create_bullet import CreateBullet
from units.effect.add_behavior import AddBehavior
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.behaviors.faith import FaithBehavior
from units.skills.tech_unlock_effect import TechUnlockEffect
from units.skills.fire_ball import FireballSkill
from auxiliary_tools.bullet_pre import BulletPre
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
import pygame


class Master(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=310, max_magic=160, magic_armor=25, physical_armor=4,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(1, 3),
                                             speed=0.9, magic_recovery_speed=1)
        super().__init__("./data/img/units/movable/master", "master", pygame.Rect(x, y, 80, 80), unit_height_c=75,
                         attribute_manager=attribute_manager, population_cost=3)
        self.flag.add_flag(["master", "land_force", "human", "magic_user"])

        self.behavior_manager.add(HMBar(width=0.7))
        self.behavior_manager.add(Shadow())

        hurt_effect_35 = Hurt(value=35, hurt_type=1)
        create_explosion = CreateSpecialEffect(effect_name="FireBlastSMALL", size=(70, 70), fps_level=1)
        bullet = BulletPre(name="fireballSMALL", effect=hurt_effect_35, direct=True, hit_effect=create_explosion,
                           speed=700, trajectory_size=(20, 20), trajectory_name="fireballSMALLT", trajectory_fps=1)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_bullet, aim_range=480, escape_range=50,
                        base_hurt=35, name="火焰冲击", hurt_describe="魔法伤害", describe="一团活化的能量而已，至少法师们是这么解释的",
                        hurt_effect=hurt_effect_35, level_up=5, fire_delay=25, interval=2.2)
        self.weapons.add(weapon)

        fireball_skill = FireballSkill(self)
        self.skill_manager.add(fireball_skill)
        self.skill_panel.replace("fireballIcon", fireball_skill, describe="火球术&对敌方非建筑单位造成140点魔法伤害",
                                 key="T", line=3, column=0, mouse=False)

        fire_spread_skill = TechUnlockEffect(self, "fire_spread")
        self.skill_manager.add(fire_spread_skill)
        self.skill_panel.replace("FireSpreadIcon", fire_spread_skill, describe="火焰扩散&火球术对主目标周围的非建筑单位"
                                                                               "额外造成70点魔法伤害",
                                 key=None, line=3, column=1, mouse=False)

        self.radar_range = 600
        self.exp_produce = 24

        self.cost = {"gold": 200, "wood": 100}
        self.base_bullet_anchor = [15, -20]

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "人类", "魔力单位")
        self.unit_panel["armor_name"] = ("法师长袍", "法师长袍")
        self.unit_panel["name"] = "法师"
        self.unit_panel["unit_icon"] = "masterIcon"
        self.unit_panel["title"] = "法师"
