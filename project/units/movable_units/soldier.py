from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.add_behavior import AddBehavior
from units.effect.mixed_effect import MixedEffect
from units.effect.create_special_effect import CreateSpecialEffect
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.behaviors.array import ArrayBehavior
from units.skills.tech_unlock_effect import TechUnlockEffect
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
import pygame


class Soldier(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=410, max_magic=0, magic_armor=0, physical_armor=8,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(2, 0),
                                             speed=1)
        super().__init__("./data/img/units/movable/soldier", "soldier", pygame.Rect(x, y, 90, 75), unit_height_c=70,
                         attribute_manager=attribute_manager, population_cost=2)
        self.flag.add_flag(["soldier", "land_force", "human"])

        self.behavior_manager.add(HMBar(width=0.6))
        self.behavior_manager.add(Shadow())

        hurt_effect_25 = Hurt(value=25, hurt_type=0)
        create_explosion = CreateSpecialEffect(effect_name="hitted", size=(60, 60), fps_level=1)
        mixed_effect = MixedEffect(effects=[hurt_effect_25, create_explosion])
        weapon_filter = Filter(self, ["unit", "enemy", "land_force"], ["air_force"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=mixed_effect, aim_range=20, escape_range=50,
                        base_hurt=30, name="挥砍", hurt_describe="物理伤害", describe="士兵们的拿手绝活",
                        hurt_effect=hurt_effect_25, level_up=4, fire_delay=25, interval=2)
        self.weapons.add(weapon)

        array_effect = AddBehavior(behavior=ArrayBehavior())
        array_skill = TechUnlockEffect(self, "array", effect=array_effect)
        self.skill_manager.add(array_skill)
        self.skill_panel.replace("arrayIcon", array_skill, describe="列阵&周围范围600内每存在一个己方士兵，造成的伤害提高6%，受到的伤"
                                                                    "害减少6%，最多叠加5次",
                                 key=None, line=3, column=0, mouse=False)

        self.cost = {"gold": 120, "wood": 35}
        self.radar_range = 600
        self.exp_produce = 10

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "人类")
        self.unit_panel["armor_name"] = ("士兵护甲", "士兵护甲")
        self.unit_panel["name"] = "士兵"
        self.unit_panel["unit_icon"] = "soldierIcon"
        self.unit_panel["title"] = "普通的士兵"
