from units.building import Building
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.bonfire_light import BonfireLight
from units.effect.add_behavior import AddBehavior
from units.skills.halo import Halo
from unit_tools.filter import Filter
from unit_tools.attribute_manager import AttributeManager
import pygame


class Bonfire(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/bonfire", "bonfire", pygame.Rect(x, y, 50, 70),
                         unit_height_c=65,
                         attribute_manager=AttributeManager(max_health=150, max_magic=0, magic_armor=0,
                                                            armor_tech=("None", "None"), physical_armor=0),
                         population_produce=0, gird_layer=1)
        self.flag.add_flag(["bon_fire"])
        self.volume = 23
        self.cost = {"gold": 20, "wood": 110}

        self.radar_range = 600

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=50))

        fire_behavior = BonfireLight()
        add_behavior = AddBehavior(behavior=fire_behavior)
        unit_filter = Filter(self, ["unit", "human"], ["enemy", "building"])
        fire_halo = Halo(self, effect=add_behavior, unit_filter=unit_filter, flag="fire_halo", influence_range=600,
                         tech_require=None)

        self.skill_manager.add(fire_halo)

        self.skill_panel.replace("bonfireHALO", fire_halo,
                                 describe="火光&周围距离600内的友方或己方人类单位生命回复速度提升1.5/秒",
                                 key=None, line=3, column=0, mouse=False)

        self.unit_panel["unit_label"] = ("建筑", "小型单位")
        self.unit_panel["armor_name"] = ("枯木", "枯木")
        self.unit_panel["name"] = "篝火"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "篝火"
        self.unit_panel["unit_icon"] = "bonfireIcon"
