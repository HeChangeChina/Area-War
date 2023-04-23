from units.movable_unit import MovableUnit
from units.behaviors.shadow import Shadow
from units.effect.add_behavior import AddBehavior
from units.effect.create_bullet import CreateBullet
from units.effect.create_special_effect import CreateSpecialEffect
from units.effect.search_range import SearchRange
from units.effect.mixed_effect import MixedEffect
from units.effect.hurt import Hurt
from units.ballistic.upper_parabola import UpperParabola
from units.ballistic.fall import Fall
from units.behaviors.hero_health_magic_bar import HeroHMBar
from units.behaviors.shock import ShockBehavior
from units.skills.self_chant import SelfChantSkill
from units.skills.chant_skill import ChantSkill
from units.skills.flash import SkillFlash
from units.skills.halo import Halo
from units.skills.learn import LearnSkill
from units.skills.ArcaneFeedBack import ArcaneFeedBackSkill
from units.behaviors.ArcaneLight import ArcaneLightBehavior
from units.sight.range_sight import RangeSight
from unit_tools.attribute_manager import AttributeManager
from unit_tools.filter import Filter
from unit_tools.filter import NullFilter
from unit_tools.weapon import Weapon
from auxiliary_tools.bullet_pre import BulletPre
from auxiliary_tools.tech_tree import TechTree
import pygame


class Lin(MovableUnit):
    def __init__(self, x, y):
        attribute = AttributeManager(max_health=350, max_magic=80, magic_armor=10, armor_tech=("lin_level", "lin_level"),
                                     armor_level_add=(1, 3), physical_armor=3, speed=1.8, magic_recovery_speed=1,
                                     exp_tech="lin_level", exp_amount_tech="lin_exp", exp_tech_team_change=True,
                                     health_recovery_speed=1.2)
        attribute.exp_level = [50, 75, 100, 150, 200, 300, 400, 600, 800, 1200, 3000]
        attribute.hm_level_up = [(20, 5), (27, 6), (35, 8), (45, 10), (58, 13), (75, 16), (92, 19), (110, 23),
                                 (130, 26), (152, 30), (200, 75)]
        super().__init__("./data/img/units/movable/lin", "lin", pygame.Rect(x, y, 50, 70), unit_height_c=62,
                         attribute_manager=attribute, population_cost=5)
        self.flag.add_flag(["lin", "hero", "human", "magic_user", "land_force", "lin"])

        self.behavior_manager.add(Shadow(shadow_size=20))
        self.behavior_manager.add(HeroHMBar(name="琳", name_c=18))

        hurt_effect_35 = Hurt(value=35, hurt_type=1)
        create_explosion = CreateSpecialEffect(effect_name="arcaneBlastNORMAL", size=(60, 60), fps_level=1)
        bullet = BulletPre(name="arcaneNORMAL", effect=hurt_effect_35, direct=False, trajectory_name="arcaneT",
                           trajectory_size=(20, 20), trajectory_fps=1, hit_effect=create_explosion)
        create_bullet = CreateBullet(bullet=bullet)
        weapon_filter = Filter(self, ["unit", "enemy"])
        weapon = Weapon(weapon_filter, tech="lin_level", effect=create_bullet, aim_range=400, base_hurt=35, name="戈林",
                        hurt_describe="魔法伤害", describe="戈林由奥术塔主掌握，对奥术魔力有很强的亲和力",
                        hurt_effect=hurt_effect_35, level_up=3, icon="goering", fire_delay=20, interval=1.5)
        self.weapons.add(weapon)

        hurt_effect_160 = Hurt(value=110, hurt_type=1)
        search_range = SearchRange(effect=hurt_effect_160, range=110, required_flag=["unit", "enemy", "land_force"])
        create_explosion = CreateSpecialEffect(effect_name="ArcaneBombBlast", size=(220, 220), fps_level=1)
        bullet = BulletPre(name="ArcaneBomb", effect=search_range, direct=False, trajectory_name="ArcaneBombT",
                           trajectory_size=(30, 30), trajectory_fps=1, hit_effect=create_explosion, fps_level=1,
                           ballistic=UpperParabola(300))
        create_bullet = CreateBullet(bullet=bullet)
        arcane_bomb_filter = NullFilter(point=True)
        arcane_bomb = ChantSkill(self, arcane_bomb_filter, cooling=7, magic_require=45, sight=RangeSight(110),
                                 effect=create_bullet, flag="arcane_bomb", quick_spell=False, chant_time=0.5,
                                 chant_animate="chant", skill_animate="skill", aiming_range=650, target_y=800,
                                 animate_advance_frame=30, tech_require="lin_arcane_bomb")
        self.skill_panel.replace("ArcaneBombI", arcane_bomb,
                                 describe="奥术炸弹&琳压缩一团奥术能量并抛出，在接触地面后对周围110半径内的所有地面敌人"
                                          "造成110点魔法伤害",
                                 key="Q", line=3, column=0, mouse=False)
        self.skill_manager.add(arcane_bomb)

        create_flash = CreateSpecialEffect(effect_name="flash", size=(80, 80), fps_level=1)
        flash_skill = SkillFlash(self, effect=create_flash, tech_require="lin_flash")
        self.skill_panel.replace("flashI", flash_skill,
                                 describe="闪现&琳汇聚奥术能量，将自身闪现至目标位置，至多闪现360距离",
                                 key="E", line=3, column=2, mouse=False)
        self.skill_manager.add(flash_skill)

        add_arcane_behavior = AddBehavior(behavior=ArcaneLightBehavior())
        unit_filter = Filter(self, ["unit", "magic_user"], ["enemy"], ["ally", "self", "own"])
        arcane_light = Halo(self, unit_filter, "arcane_light", effect=add_arcane_behavior,
                            tech_require="lin_arcane_light")
        self.skill_panel.replace("ArcaneLightI", arcane_light,
                                 describe="奥术光辉&身为奥术塔主，琳周围汇聚着奥术的能量，能提升周围友方或己方魔力单位1.5/秒的魔力回复速度",
                                 key=None, line=2, column=0, mouse=False)
        self.skill_manager.add(arcane_light)

        arcane_feed_back = ArcaneFeedBackSkill(self, "lin_arcane_feed_back")
        self.skill_panel.replace("ArcaneFeedBackI", arcane_feed_back,
                                 describe="奥术反馈&琳在消耗魔力时，会反馈于自身，每消耗30点法力会使自身伤害提升10%，"
                                          "至多叠加3次，持续6秒",
                                 key=None, line=3, column=3, mouse=False)
        self.skill_manager.add(arcane_feed_back)

        pre_effect = CreateSpecialEffect(effect_name="ShockPre", size=(300, 300), fps_level=1)
        shock_effect = CreateSpecialEffect(effect_name="shock", size=(300, 300), fps_level=1, index=-11)
        shocked_effect = CreateSpecialEffect(effect_name="shocked", size=(60, 60), fps_level=1)
        hurt_effect_70 = Hurt(value=70, hurt_type=1)
        shock_behavior_add = AddBehavior(behavior=ShockBehavior())
        shock_hurt_mixed_effect = MixedEffect(effects=[hurt_effect_70, shock_behavior_add, shocked_effect])
        shock_search_range = SearchRange(effect=shock_hurt_mixed_effect, range=150, required_flag=["unit", "enemy"],
                                         excluded_flag=["building"])
        shock_mixed_effect = MixedEffect(effects=[shock_effect, shock_search_range])
        shock_skill = SelfChantSkill(self, quick_spell=False, cooling=12, magic_require=60,
                                     effect=shock_mixed_effect, flag="shock", chant_time=1.1,
                                     chant_animate="chant", skill_animate="skill", animate_advance_frame=30,
                                     pre_effect=pre_effect, tech_require="lin_shock")
        self.skill_panel.replace("shockI", shock_skill,
                                 describe="震撼&琳凝聚奥术能量，在周围半径150的范围内引爆，对范围内的敌方非建筑单位造"
                                          "成70点魔法伤害，并降低他们的移动速度与攻击速度，持续8秒",
                                 key="W", line=3, column=1, mouse=False)
        self.skill_manager.add(shock_skill)

        arcane_star_hurt = Hurt(value=450, hurt_type=1)
        arcane_star_hurt_center = Hurt(value=250, hurt_type=2)
        arcane_star_hurt_building = Hurt(value=500, hurt_type=0)
        arcane_star_search = SearchRange(effect=arcane_star_hurt, range=450, required_flag=["unit"], circle=False)
        arcane_star_center_search = SearchRange(effect=arcane_star_hurt_center, range=250, required_flag=["unit"],
                                                circle=False)
        arcane_star_building_search = SearchRange(effect=arcane_star_hurt_building, range=450,
                                                  required_flag=["unit", "building"], circle=False)
        arcane_star_filter = NullFilter(point=True)
        arcane_star_explosion = CreateSpecialEffect(effect_name="ArcaneStarExplosion", size=(900, 300), fps_level=1)
        arcane_star_pre = CreateSpecialEffect(effect_name="ArcaneStarPre", size=(900, 250), fps_level=1)
        explosion_mixed = MixedEffect(effects=[arcane_star_search, arcane_star_center_search,
                                               arcane_star_building_search, arcane_star_explosion])
        bullet = BulletPre(name="ArcaneStarBullet", effect=explosion_mixed, direct=False, trajectory_name="ArcaneStarT",
                           trajectory_size=(200, 200), trajectory_fps=0, ballistic=Fall(), fps_level=1,
                           trajectory_shift=-20, trajectory_cycle=8)
        create_bullet = CreateBullet(bullet=bullet)
        arcane_star_skill = ChantSkill(self, arcane_star_filter, cooling=150, magic_require=120, sight=RangeSight(450),
                                       effect=create_bullet, flag="arcane_star", quick_spell=False, chant_time=3,
                                       chant_animate="chant", skill_animate="skill", aiming_range=800, target_y=800,
                                       animate_advance_frame=30, pre_effect=arcane_star_pre,
                                       tech_require="lin_arcane_star")
        self.skill_panel.replace("ArcaneStarI", arcane_star_skill,
                                 describe="天启&琳沟通奥术之星，对目标点降下它的投影，对落点范围450内的所有单位造成450点魔法"
                                          "伤害，建筑目标会额外受到500点物理伤害，落点范围250内单位会额外受到250点真实伤害",
                                 key="R", line=3, column=4, mouse=False)
        self.skill_manager.add(arcane_star_skill)

        self.skill_panel.replace("learnIcon", None,
                                 describe="学习&琳在1,2,4,6,8,10级时，可以额外学习一个技能('天启'需要琳至少达到8级才可以学习)",
                                 key="L", line=2, column=4, mouse=False, panel_to="learn")
        self.skill_panel.replace("SkillCancel", None,
                                 describe="返回&返回主面板", panel="learn",
                                 key="B", line=3, column=4, mouse=False, panel_to="defeat")

        learn_arcane_bomb = LearnSkill(self, "lin_level", 2, "lin_skill_point", "lin_arcane_bomb", 0, 2,
                                       "learn_arcane_bomb")
        self.skill_manager.add(learn_arcane_bomb)
        self.skill_panel.replace("ArcaneBombI", learn_arcane_bomb,
                                 describe="学习-奥术炸弹&琳压缩一团奥术能量并抛出，在接触地面后对周围110半径内的所有地面敌人"
                                          "造成110点魔法伤害", panel="learn",
                                 key="Q", line=0, column=0, mouse=False)
        learn_flash = LearnSkill(self, "lin_level", 2, "lin_skill_point", "lin_flash", 0, 2,
                                       "learn_flash")
        self.skill_manager.add(learn_flash)
        self.skill_panel.replace("flashI", learn_flash,
                                 describe="学习-闪现&琳汇聚奥术能量，将自身闪现至目标位置，至多闪现360距离", panel="learn",
                                 key="E", line=0, column=2, mouse=False)
        learn_arcane_light = LearnSkill(self, "lin_level", 2, "lin_skill_point", "lin_arcane_light", 0, 2,
                                        "learn_arcane_light")
        self.skill_manager.add(learn_arcane_light)
        self.skill_panel.replace("ArcaneLightI", learn_arcane_light,
                                 describe="学习-奥术光辉&身为奥术塔主，琳周围汇聚着奥术的能量，能提升周围友方或己方魔力单位1.5/秒的魔力回复速度"
                                 , panel="learn", key="Z", line=1, column=0, mouse=False)
        learn_shock = LearnSkill(self, "lin_level", 2, "lin_skill_point", "lin_shock", 0, 2,
                                 "learn_shock")
        self.skill_manager.add(learn_shock)
        self.skill_panel.replace("shockI", learn_shock,
                                 describe="学习-震撼&琳凝聚奥术能量，在周围半径150的范围内引爆，对范围内的敌方非建筑单位造"
                                          "成70点魔法伤害，并降低他们的移动速度与攻击速度，持续8秒", panel="learn",
                                 key="W", line=0, column=1, mouse=False)
        learn_arcane_star = LearnSkill(self, "lin_level", 2, "lin_skill_point", "lin_arcane_star", 8, 2,
                                       "learn_arcane_star")
        self.skill_manager.add(learn_arcane_star)
        self.skill_panel.replace("ArcaneStarI", learn_arcane_star,
                                 describe="学习-天启&琳沟通奥术之星，对目标点降下它的投影，对落点范围450内的所有单位造成450点魔法"
                                          "伤害，建筑目标会额外受到500点物理伤害，落点范围250内单位会额外受到250点真实"
                                          "伤害&(需要琳达到8级)", panel="learn",
                                 key="R", line=0, column=4, mouse=False)
        learn_arcane_feed_back = LearnSkill(self, "lin_level", 2, "lin_skill_point", "lin_arcane_feed_back", 0, 2,
                                            "learn_arcane_feed_back")
        self.skill_manager.add(learn_arcane_feed_back)
        self.skill_panel.replace("ArcaneFeedBackI", learn_arcane_feed_back,
                                 describe="学习-奥术反馈&琳在消耗魔力时，会反馈于自身，每消耗30点法力会使自身伤害提升10%，"
                                          "至多叠加3次，持续6秒", panel="learn",
                                 key="X", line=0, column=3, mouse=False)

        self.volume = 20

        self.visual_field = 800
        self.radar_range = 600

        self.order = 2

        self.base_bullet_anchor = [20, -20]

        self.unit_panel["unit_label"] = ("人类", "英雄单位", "魔力单位")
        self.unit_panel["armor_icon"] = ("MagicArmorP", "MagicRobesM")
        self.unit_panel["armor_name"] = ("魔力护甲", "大法师之袍")
        self.unit_panel["name"] = "琳"
        self.unit_panel["unit_icon"] = "linIcon"
        self.unit_panel["base_info"] = 80
        self.unit_panel["exp_info"] = 10
        self.unit_panel["title"] = "奥兰城最年轻的奥术塔主"

        self.if_start = False

        self.level = 999

    def change_team(self, team):
        super().change_team(team)
        if self.if_start is False:
            self.if_start = True
            TechTree.add_level("lin_count", team, 1)

    def clear(self):
        TechTree.add_level("lin_count", self.team, -1)
        super().clear()

    def update_60(self):
        # print(self.attribute_manager.get_attribute("harm_cause_rate"))
        if self.level < self.attribute_manager.level:
            create_effect = CreateSpecialEffect(effect_name="LevelUp", size=(60, 100), fps_level=1)
            create_effect.take_effect(self, self)
        self.level = self.attribute_manager.level
