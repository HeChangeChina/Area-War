from units.building import Building
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from units.skills.produce import ProduceSkill
from unit_tools.attribute_manager import AttributeManager
from units.behaviors.produce_lists_shower import ProduceListShower
import pygame


class HeroAltar(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/HeroAltar", "HeroAltar", pygame.Rect(x, y, 150, 400),
                         unit_height_c=398,
                         attribute_manager=AttributeManager(max_health=700, max_magic=0, magic_armor=0,
                                                            armor_tech=("masonry", "masonry"), physical_armor=6),
                         population_produce=0)
        self.flag.add_flag(["hero_altar", "production_unit"])
        self.volume = 70
        self.cost = {"gold": 80, "wood": 130}

        cost = {"gold": 300}
        produce_lin = ProduceSkill(self, "lin", "linIcon", cost, 5, 60, animate="produce", flag="lin",
                                   tech_require="lin_count", tech_mode="not_have")
        self.skill_manager.add(produce_lin)
        self.skill_panel.replace("LinPIcon", produce_lin, describe="召唤/复活-琳&用时:60s&琳是奥兰城最年轻的奥术塔主"
                                                                   "，琳的奥术魔法可以对大范围的地方地面单位造成极强"
                                                                   "的压制效果",
                                 key="Q", line=3, column=0, mouse=False)

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=70))
        self.behavior_manager.add(ProduceListShower())

        self.unit_panel["unit_label"] = ("建筑", "中型单位")
        self.unit_panel["armor_name"] = ("石制雕像", "石制雕像")
        self.unit_panel["name"] = "英雄祭坛"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "英雄祭坛"
        self.unit_panel["unit_icon"] = "HeroAltar"
