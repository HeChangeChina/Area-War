from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.search_range import SearchRange
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.create_bullet import CreateBullet
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.ballistic.upper_parabola import UpperParabola
from auxiliary_tools.bullet_pre import BulletPre
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
import pygame


class TruthTeller(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=850, max_magic=0, magic_armor=10, physical_armor=8,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(2, 3),
                                             speed=1.2)
        super().__init__("./data/img/units/movable/TruthTeller", "TruthTeller", pygame.Rect(x, y, 400, 250), unit_height_c=248,
                         attribute_manager=attribute_manager, population_cost=6)
        self.height_controller.change_mode(2)
        self.height_controller.target_height = 750
        self.flag.add_flag(["truth_teller", "air_force", "machine"])

        self.behavior_manager.add(HMBar(width=0.7))
        self.behavior_manager.add(Shadow(shadow_size=180))
        self.volume = 180

        hurt_effect_145 = Hurt(value=145, hurt_type=0)
        create_explosion = CreateSpecialEffect(effect_name="FireBlastMIDDLE", size=(80, 80), fps_level=1)
        bullet = BulletPre(name="shell", effect=hurt_effect_145, direct=False, hit_effect=create_explosion, speed=1800)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy", "land_force"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_bullet, aim_range=300, escape_range=50,
                        base_hurt=145, name="说服者", hurt_describe="物理伤害", describe="这门大口径的主炮主要负责向地面"
                                                                                 "敌人传递真理",
                        hurt_effect=hurt_effect_145, level_up=10, fire_delay=15, interval=3, fire_animate="fire",
                        mode="additional")
        self.weapons.add(weapon)

        hurt_effect_21 = Hurt(value=21, hurt_type=0)
        search_range = SearchRange(effect=hurt_effect_21, range=35, required_flag=["unit", "enemy", "land_force"])
        create_explosion = CreateSpecialEffect(effect_name="FireBlastSMALL", size=(70, 70), fps_level=1)
        bullet = BulletPre(name="bomb", effect=search_range, direct=False, hit_effect=create_explosion, speed=600,
                           ballistic=UpperParabola(250), fps_level=0)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy", "land_force"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_bullet, aim_range=200, escape_range=50,
                        base_hurt=21, name="投掷炸弹", hurt_describe="物理伤害", describe="\"投弹!快点投弹!\"，炸弹可以"
                                                                                  "轰炸小范围的敌人",
                        hurt_effect=hurt_effect_21, level_up=3, fire_delay=0, interval=1.1, fire_animate=None,
                        mode="additional")
        self.weapons.add(weapon)

        self.cost = {"gold": 350, "wood": 450}
        self.base_bullet_anchor = [0, 30]
        self.exp_produce = 65

        self.unit_panel["unit_label"] = ("大型单位", "重型单位", "机械")
        self.unit_panel["armor_name"] = ("铁皮外壳", "铁皮外壳")
        self.unit_panel["name"] = "真理叙说者"
        self.unit_panel["unit_icon"] = "TruthTellerIcon"
        self.unit_panel["title"] = "真理叙说者"
