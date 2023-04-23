from units.building import Building
from units.skills.produce import ProduceSkill
from units.skills.research import ResearchSkill
from units.effect.unlock_tech import UnlockTech
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.produce_lists_shower import ProduceListShower
from unit_tools.attribute_manager import AttributeManager
from auxiliary_tools.tech_tree import TechTree
import pygame


class MagicCollege(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/MagicCollege", "MagicCollege", pygame.Rect(x, y, 250, 250),
                         unit_height_c=248,
                         attribute_manager=AttributeManager(max_health=1050, max_magic=0, magic_armor=10,
                                                            armor_tech=("masonry", "masonry"), physical_armor=4),
                         population_produce=0)
        self.flag.add_flag(["magic_college", "production_unit"])
        self.volume = 120
        self.cost = {"gold": 250, "wood": 120}

        cost = {"gold": 200, "wood": 75}
        produce_minister = ProduceSkill(self, "minister", "ministerIcon", cost, 3, 28, animate="produce", flag="minister")
        self.skill_manager.add(produce_minister)
        self.skill_panel.replace("ministerPIcon", produce_minister, describe="训练-牧师&用时:28s&牧师凭借一手治疗术成为了"
                                                                             "战场上最受欢迎的盟友，拥有初始技能\"治疗术\"",
                                 key="Q", line=3, column=0, mouse=False)

        cost = {"gold": 200, "wood": 100}
        produce_master = ProduceSkill(self, "master", "masterIcon", cost, 3, 28, animate="produce",
                                      flag="master")
        self.skill_manager.add(produce_master)
        self.skill_panel.replace("masterPIcon", produce_master, describe="训练-法师&用时:28s&法师们可以对敌方造成大量"
                                                                           "的法术伤害，拥有初始技能\"火球术\"",
                                 key="W", line=3, column=1, mouse=False)

        cost = {"gold": 100, "wood": 100}
        unlock_faith = UnlockTech(tech="faith")
        unlock_faithS = ResearchSkill(self, cost, "faithIcon", unlock_faith, time_requirement=30,
                                      flag="unlock_faith", tech_require="faith", tech_mode="not have")
        self.skill_manager.add(unlock_faithS)
        self.skill_panel.replace("faithIcon", unlock_faithS, describe="研究-虔诚信仰&用时:30s&牧师的最大法力值增加50",
                                 key="Z", line=2, column=0, mouse=False)

        cost = {"gold": 100, "wood": 100}
        unlock_fire_spread = UnlockTech(tech="fire_spread")
        unlock_fire_spreadS = ResearchSkill(self, cost, "FireSpreadIcon", unlock_fire_spread, time_requirement=45,
                                      flag="unlock_fire_spread", tech_require="fire_spread", tech_mode="not have")
        self.skill_manager.add(unlock_fire_spreadS)
        self.skill_panel.replace("FireSpreadIcon", unlock_fire_spreadS, describe="研究-火焰扩散&用时:45s&法师的火球术可以额外对主目"
                                                                                 "标周围半径50内的非建筑敌人造成70点魔法伤害",
                                 key="X", line=2, column=1, mouse=False)

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=120))
        self.behavior_manager.add(ProduceListShower())

        self.unit_panel["unit_label"] = ("建筑", "大型单位")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "魔法学院"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "魔法学院"
        self.unit_panel["unit_icon"] = "MagicCollegeIcon"

        self.if_build_complete = False

    def finish_build(self):
        super().finish_build()
        self.if_build_complete = True
        TechTree.add_level("magic_college_count", self.team, 1)

    def clear(self):
        if self.if_build_complete:
            TechTree.add_level("magic_college_count", self.team, -1)
        super().clear()
