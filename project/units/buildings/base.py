from units.building import Building
from units.skills.produce import ProduceSkill
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.produce_lists_shower import ProduceListShower
from unit_tools.attribute_manager import AttributeManager
import pygame


class Base(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/base", "base", pygame.Rect(x, y, 400, 230),
                         unit_height_c=228,
                         attribute_manager=AttributeManager(max_health=2200, max_magic=0, magic_armor=10,
                                                            armor_tech=("masonry", "masonry"), physical_armor=13),
                         population_produce=16)
        self.flag.add_flag(["base", "production_unit", "storehouse"])
        self.volume = 170
        self.cost = {"gold": 500, "wood": 350}

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=180))
        self.behavior_manager.add(ProduceListShower())

        cost = {"gold": 80}
        skill_produce = ProduceSkill(self, "worker", "workerIcon", cost, 1, 15, animate="produce", flag="worker")
        self.skill_manager.add(skill_produce)
        self.skill_panel.replace("workerPIcon", skill_produce, describe="生产-矮人工匠&用时:15s&矮人工匠们拥有着最高超的建筑手艺，"
                                                                         "他们可以快速的建起与修理任何建筑，同时，他们"
                                                                        "也可以采集各种资源(现仅包含树木)",
                                 key="F", line=3, column=0, mouse=False)

        self.unit_panel["unit_label"] = ("建筑", "大型单位", "资源存放点")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "基地"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "指挥中心"
        self.unit_panel["unit_icon"] = "baseIcon"
