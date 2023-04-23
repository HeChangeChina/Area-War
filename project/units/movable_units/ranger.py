from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.create_bullet import CreateBullet
from units.effect.add_behavior import AddBehavior
from units.effect.mixed_effect import MixedEffect
from units.ballistic.upper_parabola import UpperParabola
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.behaviors.poisoning import Poisoning
from units.skills.tech_unlock_effect import TechUnlockEffect
from auxiliary_tools.bullet_pre import BulletPre
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
import pygame


class Ranger(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=160, max_magic=0, magic_armor=10, physical_armor=4,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(2, 2),
                                             speed=1.7)
        super().__init__("./data/img/units/movable/ranger", "ranger", pygame.Rect(x, y, 60, 70), unit_height_c=65,
                         attribute_manager=attribute_manager, population_cost=2)
        self.flag.add_flag(["ranger", "land_force", "human"])

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow())

        hurt_effect_18 = Hurt(value=18, hurt_type=0)
        po_effect = AddBehavior(behavior=Poisoning())
        hurt_mixed_effect = MixedEffect(effects=[hurt_effect_18, (po_effect, "envenomed")])
        create_explosion = CreateSpecialEffect(effect_name="hitted", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="arrow", effect=hurt_mixed_effect, direct=True, hit_effect=create_explosion,
                           ballistic=UpperParabola(50))
        create_arrow = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_arrow, aim_range=350, escape_range=50,
                        base_hurt=18, name="精灵木弓", hurt_describe="物理伤害", describe="精灵们拥有着百发百中的箭术",
                        hurt_effect=hurt_effect_18, level_up=3, fire_delay=25, interval=1.8, fire_animate="shoot",
                        aiming_animate="PrepareShoot", additional_tech="master_ranger",
                        additional_attribute={"aim_range": 150})
        self.weapons.add(weapon)

        envenomed_skill = TechUnlockEffect(self, "envenomed")
        self.skill_manager.add(envenomed_skill)
        self.skill_panel.replace("envenomedIcon", envenomed_skill, describe="淬毒武器&攻击命中可以使敌人中毒，每层中毒效"
                                                                            "果减低目标2点物理护甲，并使目标每秒受到2点真实伤"
                                                                            "害，至多叠加3层，持续7秒",
                                 key=None, line=3, column=1, mouse=False)

        master_ranger_skill = TechUnlockEffect(self, "master_ranger")
        self.skill_manager.add(master_ranger_skill)
        self.skill_panel.replace("MasterRangerIcon", master_ranger_skill, describe="大师级游侠训练&攻击距离增加150",
                                 key=None, line=3, column=0, mouse=False)

        self.cost = {"gold": 90, "wood": 65}
        self.base_bullet_anchor = [30, -20]
        self.exp_produce = 8

        self.visual_field = 650
        self.radar_range = 650

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "人类")
        self.unit_panel["armor_name"] = ("游侠披风", "游侠披风")
        self.unit_panel["name"] = "游侠"
        self.unit_panel["unit_icon"] = "rangerIcon"
        self.unit_panel["title"] = "游侠"
