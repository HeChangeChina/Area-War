from units.building import Building
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from units.effect.hurt import Hurt
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.create_bullet import CreateBullet
from units.ballistic.upper_parabola import UpperParabola
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
from auxiliary_tools.bullet_pre import BulletPre
import pygame


class Bartizan(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/bartizan", "bartizan", pygame.Rect(x, y, 100, 250),
                         unit_height_c=248,
                         attribute_manager=AttributeManager(max_health=850, max_magic=0, magic_armor=10,
                                                            armor_tech=("masonry", "masonry"), physical_armor=7),
                         population_produce=0)
        self.flag.add_flag(["bartizan"])
        self.volume = 45
        self.cost = {"gold": 90, "wood": 110}

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=45))
        self.visual_field = 550
        self.radar_range = 550

        hurt_effect_32 = Hurt(value=32, hurt_type=0)
        create_explosion = CreateSpecialEffect(effect_name="hitted", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="arrowBIG", effect=hurt_effect_32, direct=True, hit_effect=create_explosion, speed=1000)
        create_arrow = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy"])
        weapon = Weapon(weapon_filter, tech="None", effect=create_arrow, aim_range=500, escape_range=50,
                        base_hurt=32, name="弩箭", hurt_describe="物理伤害", describe="弩箭是箭塔内的标配",
                        hurt_effect=hurt_effect_32, level_up=3, fire_delay=25, interval=1.5, fire_animate="defeat",
                        aiming_animate="defeat")
        self.weapons.add(weapon)

        self.base_bullet_anchor = [0, -80]
        self.exp_produce = 15

        self.unit_panel["unit_label"] = ("建筑", "中型单位")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "箭塔"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "箭塔"
        self.unit_panel["unit_icon"] = "bartizanIcon"
