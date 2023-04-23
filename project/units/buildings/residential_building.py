from units.building import Building
from units.skills.research import ResearchSkill
from units.effect.add_resource import AddResource
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from unit_tools.attribute_manager import AttributeManager
import pygame


class ResidentialBuilding(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/ResidentialBuilding", "ResidentialBuilding", pygame.Rect(x, y, 100, 100),
                         unit_height_c=98,
                         attribute_manager=AttributeManager(max_health=450, max_magic=0, magic_armor=0,
                                                            armor_tech=("masonry", "masonry"), physical_armor=5),
                         population_produce=8)
        self.flag.add_flag(["residential_building"])
        self.volume = 50
        self.cost = {"gold": 130, "wood": 80}

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=50))

        cost = {}
        add_resource_effect = AddResource(resource_type="gold", value=20)
        produce_gold = ResearchSkill(self, cost, "goldIcon", add_resource_effect, time_requirement=10,
                                     flag="produce_gold", auto_use=True, idle_use=True)
        self.skill_manager.add(produce_gold)
        self.skill_panel.replace("goldPIcon", produce_gold, describe="交税&用时:10s&上交20点金币税收",
                                 key="Q", line=3, column=0, mouse=False)

        self.unit_panel["unit_label"] = ("建筑", "中型单位")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "居民楼"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "居民楼"
        self.unit_panel["unit_icon"] = "ResidentialBuildingIcon"
