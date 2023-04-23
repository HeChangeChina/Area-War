from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.create_bullet import CreateBullet
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from auxiliary_tools.bullet_pre import BulletPre
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
import pygame


class FlyMachine(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=340, max_magic=0, magic_armor=0, physical_armor=6,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(2, 0),
                                             speed=1.4)
        super().__init__("./data/img/units/movable/FlyMachine", "FlyMachine", pygame.Rect(x, y, 130, 130), unit_height_c=128,
                         attribute_manager=attribute_manager, population_cost=3)
        self.height_controller.change_mode(2)
        self.height_controller.target_height = 650
        self.flag.add_flag(["musketeer", "air_force", "machine"])

        self.behavior_manager.add(HMBar(width=0.7))
        self.behavior_manager.add(Shadow(shadow_size=50))
        self.volume = 50
        self.exp_produce = 24

        hurt_effect_30 = Hurt(value=33, hurt_type=0)
        create_explosion = CreateSpecialEffect(effect_name="hitted", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="bullet", effect=hurt_effect_30, direct=True, hit_effect=create_explosion, speed=1800)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy", "land_force"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_bullet, aim_range=260, escape_range=50,
                        base_hurt=33, name="对地火炮模式", hurt_describe="物理伤害", describe="牺牲部分武器速度，旋转炮口，对地面敌人射击",
                        hurt_effect=hurt_effect_30, level_up=4, fire_delay=15, interval=2.4, fire_animate="AttackGround")
        self.weapons.add(weapon)

        hurt_effect_30 = Hurt(value=33, hurt_type=0)
        create_explosion = CreateSpecialEffect(effect_name="hitted", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="bullet", effect=hurt_effect_30, direct=True, hit_effect=create_explosion, speed=1800)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy", "air_force"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_bullet, aim_range=560, escape_range=50,
                        base_hurt=33, name="对空火炮模式", hurt_describe="物理伤害", describe="飞行员们喜爱速度与激情，"
                                                                                    "但他们简陋的飞行机器没有速度",
                        hurt_effect=hurt_effect_30, level_up=4, fire_delay=15, interval=1.6,
                        fire_animate="attack")
        self.weapons.add(weapon)

        self.cost = {"gold": 130, "wood": 150}
        self.base_bullet_anchor = [20, 0]

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "机械")
        self.unit_panel["armor_name"] = ("铁皮外壳", "铁皮外壳")
        self.unit_panel["name"] = "飞行机器"
        self.unit_panel["unit_icon"] = "FlyMachineIcon"
        self.unit_panel["title"] = "飞行机器"
