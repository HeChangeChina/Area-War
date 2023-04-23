from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.search_range import SearchRange
from units.effect.add_behavior import AddBehavior
from units.effect.mixed_effect import MixedEffect
from units.effect.create_special_effect import CreateSpecialEffect
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.behaviors.roar import RoarBehavior
from units.skills.self_chant import SelfChantSkill
from units.skills.tech_unlock_effect import TechUnlockEffect
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
from auxiliary_tools.tech_tree import TechTree
from random import choice
import pygame


class Knight(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=1050, max_magic=100, magic_armor=20, physical_armor=13,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(3, 5),
                                             speed=1.1)
        super().__init__("./data/img/units/movable/knight", "knight", pygame.Rect(x, y, 250, 140), unit_height_c=120,
                         attribute_manager=attribute_manager, population_cost=6)
        self.flag.add_flag(["knight", "land_force", "human"])

        self.behavior_manager.add(HMBar(width=0.5))
        self.behavior_manager.add(Shadow(shadow_size=40))

        hurt_effect_110 = Hurt(value=110, hurt_type=0)
        hurt_effect_50 = Hurt(value=50, hurt_type=0)
        search_range = SearchRange(effect=hurt_effect_50, range=80, required_flag=["unit", "enemy", "land_force"],
                                   target_included=False)
        create_explosion = CreateSpecialEffect(effect_name="KnightHit", size=(300, 120), fps_level=1)
        mixed_effect = MixedEffect(effects=[hurt_effect_110, create_explosion, search_range])
        weapon_filter = Filter(self, ["unit", "enemy", "land_force"], ["air_force"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=mixed_effect, aim_range=70, escape_range=60,
                        base_hurt=110, name="精钢长枪", hurt_describe="物理伤害", describe="抬手，戳出，然后贯穿一切敌人",
                        hurt_effect=hurt_effect_110, level_up=13, fire_delay=40, interval=2.3)
        self.weapons.add(weapon)

        edge_skill = TechUnlockEffect(self, tech="edge")
        self.skill_manager.add(edge_skill)
        self.skill_panel.replace("edge", edge_skill, describe="刃锋&攻击对主目标周围的敌人额外造成50点物理伤害",
                                 key=None, line=3, column=0, mouse=False)

        roar_effect = CreateSpecialEffect(effect_name="roar", size=(300, 300), fps_level=1, index=-11)
        roar_behavior = AddBehavior(behavior=RoarBehavior())
        roar_search_range = SearchRange(effect=roar_behavior, range=600, required_flag=["unit", "own"],
                                        excluded_flag=["enemy"], circle=False)
        roar_mix = MixedEffect(effects=[roar_effect, roar_search_range])
        roar_skill = SelfChantSkill(self, quick_spell=False, cooling=20, magic_require=70,
                                    effect=roar_mix, flag="roar", chant_time=0,
                                    chant_animate="defeat", skill_animate="defeat", animate_advance_frame=0,
                                    tech_require="roar", tech_mode="have")
        self.skill_panel.replace("roarIcon", roar_skill,
                                 describe="战吼&周围600范围内的友方单位造成伤害提升25%，持续20秒",
                                 key="W", line=3, column=1, mouse=False)
        self.skill_manager.add(roar_skill)

        self.cost = {"gold": 450, "wood": 300}
        self.radar_range = 800
        self.visual_field = 600
        self.volume = 40
        self.exp_produce = 60
        self.layer = 0

        self.unit_panel["unit_label"] = ("中型单位", "重型单位", "人类")
        self.unit_panel["armor_name"] = ("精铁护甲", "精铁护甲")
        name_list = ["艾伯", "阿道夫", "阿尔文", "亚历士", "巴奈特", "班尼", "布鲁克", "拜伦", "塞西尔"]
        self.unit_panel["name"] = "\"大块头\"" + choice(name_list)
        self.unit_panel["unit_icon"] = "knightIcon"
        self.unit_panel["title"] = "历经百战的骑士"

    def change_team(self, team):
        super().change_team(team)
        TechTree.set_level("edge", self.team, 1)
