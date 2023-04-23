from units.movable_unit import MovableUnit
from units.effect.hurt import Hurt
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.create_bullet import CreateBullet
from units.effect.add_behavior import AddBehavior
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
from units.behaviors.faith import FaithBehavior
from units.skills.tech_unlock_effect import TechUnlockEffect
from units.skills.heal import HealSkill
from auxiliary_tools.bullet_pre import BulletPre
from unit_tools.attribute_manager import AttributeManager
from unit_tools.weapon import Weapon
from unit_tools.filter import Filter
import pygame


class Minister(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=260, max_magic=150, magic_armor=25, physical_armor=4,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(1, 3),
                                             speed=0.9, magic_recovery_speed=1)
        super().__init__("./data/img/units/movable/minister", "minister", pygame.Rect(x, y, 80, 80), unit_height_c=75,
                         attribute_manager=attribute_manager, population_cost=3)
        self.flag.add_flag(["musketeer", "land_force", "human", "magic_user"])

        self.behavior_manager.add(HMBar(width=0.7))
        self.behavior_manager.add(Shadow())

        hurt_effect_25 = Hurt(value=25, hurt_type=1)
        create_explosion = CreateSpecialEffect(effect_name="light", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="lightBullet", effect=hurt_effect_25, direct=False, hit_effect=create_explosion,
                           speed=600, trajectory_size=(40, 40), trajectory_name="lightT", trajectory_fps=0)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy"])
        weapon = Weapon(weapon_filter, tech="human_weapon", effect=create_bullet, aim_range=480, escape_range=50,
                        base_hurt=25, name="惩戒", hurt_describe="魔法伤害", describe="圣光既可以治愈盟友，也可以惩戒敌人",
                        hurt_effect=hurt_effect_25, level_up=4, fire_delay=25, interval=2.6)
        self.weapons.add(weapon)

        faith_effect = AddBehavior(behavior=FaithBehavior())
        faith_skill = TechUnlockEffect(self, "faith", effect=faith_effect)
        self.skill_manager.add(faith_skill)
        self.skill_panel.replace("faithIcon", faith_skill, describe="虔诚信仰&最大法力值增加50",
                                 key=None, line=3, column=1, mouse=False)

        heal_skill = HealSkill(self)
        self.skill_manager.add(heal_skill)
        self.skill_panel.replace("healIcon", heal_skill,
                                 describe="治疗术&治疗一个友方或己方人类单位35点生命值",
                                 key="Q", line=3, column=0, mouse=False)

        self.exp_produce = 20
        self.cost = {"gold": 200, "wood": 75}
        self.base_bullet_anchor = [0, -40]

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "人类", "魔力单位")
        self.unit_panel["armor_name"] = ("神职者制式法袍", "神职者制式法袍")
        self.unit_panel["name"] = "牧师"
        self.unit_panel["unit_icon"] = "ministerIcon"
        self.unit_panel["title"] = "牧师"
