from units.building import Building
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from unit_tools.attribute_manager import AttributeManager
import pygame


class Storehouse(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/storehouse", "storehouse", pygame.Rect(x, y, 150, 100),
                         unit_height_c=98,
                         attribute_manager=AttributeManager(max_health=450, max_magic=0, magic_armor=0,
                                                            armor_tech=("masonry", "masonry"), physical_armor=6),
                         population_produce=0)
        self.flag.add_flag(["storehouse", "storehouse_building"])
        self.volume = 70
        self.cost = {"gold": 60, "wood": 80}

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=70))

        self.unit_panel["unit_label"] = ("建筑", "中型单位", "资源存放点")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "仓库"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "仓库"
        self.unit_panel["unit_icon"] = "storehouseIcon"
