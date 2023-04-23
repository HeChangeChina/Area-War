from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.create_bullet import CreateBullet
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.skills.tech_unlock_effect import TechUnlockEffect
from auxiliary_tools.bullet_pre import BulletPre
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
import pygame


class Musketeer(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=250, max_magic=0, magic_armor=15, physical_armor=6,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(2, 3),
                                             speed=0.9)
        super().__init__("./data/img/units/movable/musketeer", "musketeer", pygame.Rect(x, y, 100, 80), unit_height_c=75,
                         attribute_manager=attribute_manager, population_cost=3)
        self.flag.add_flag(["musketeer", "land_force", "human"])

        self.behavior_manager.add(HMBar(width=0.5))
        self.behavior_manager.add(Shadow())

        rifle_skill = TechUnlockEffect(self, "rifle")
        self.skill_manager.add(rifle_skill)
        self.skill_panel.replace("rifleIcon", rifle_skill, describe="膛线改良&攻击间隔减少30%",
                                 key=None, line=3, column=0, mouse=False)

        hurt_effect_40 = Hurt(value=40, hurt_type=0)
        create_explosion = CreateSpecialEffect(effect_name="hitted", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="bullet", effect=hurt_effect_40, direct=True, hit_effect=create_explosion, speed=1800)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_bullet, aim_range=430, escape_range=50,
                        base_hurt=40, name="火枪", hurt_describe="物理伤害", describe="火药燃烧的硝烟味是火枪手们的最爱",
                        hurt_effect=hurt_effect_40, level_up=6, fire_delay=25, interval=2.4, fire_animate="shoot",
                        aiming_animate="aim", additional_tech="rifle", additional_attribute={"interval": -0.72})
        self.weapons.add(weapon)

        self.exp_produce = 18
        self.cost = {"gold": 170, "wood": 50}
        self.base_bullet_anchor = [60, -20]

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "人类")
        self.unit_panel["armor_name"] = ("皮甲", "皮甲")
        self.unit_panel["name"] = "火枪手"
        self.unit_panel["unit_icon"] = "musketeerIcon"
        self.unit_panel["title"] = "火枪手"
