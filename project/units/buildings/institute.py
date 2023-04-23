from units.building import Building
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.produce_lists_shower import ProduceListShower
from units.effect.unlock_tech import UnlockTech
from units.skills.research import ResearchSkill
from unit_tools.attribute_manager import AttributeManager
from auxiliary_tools.tech_tree import TechTree
import pygame


class Institute(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/institute", "institute", pygame.Rect(x, y, 300, 240),
                         unit_height_c=238,
                         attribute_manager=AttributeManager(max_health=1100, max_magic=0, magic_armor=10,
                                                            armor_tech=("masonry", "masonry"), physical_armor=9),
                         population_produce=0)
        self.flag.add_flag(["institute"])
        self.volume = 115
        self.cost = {"gold": 270, "wood": 140}

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=115))
        self.behavior_manager.add(ProduceListShower())

        cost = {"gold": 120, "wood": 120}
        knight = UnlockTech(tech="unlock_knight")
        knight_research = ResearchSkill(self, cost, "knightPIcon", knight, time_requirement=30,
                                           flag="unlock_knight", animate="produce")
        self.skill_manager.add(knight_research)
        self.skill_panel.replace("envenomedIcon", knight_research, describe="研究-生物基因改良&用时:30s&允许训练场训"
                                                                               "练\"大块头\"",
                                 key="Z", line=3, column=0, mouse=False)

        cost = {"gold": 120, "wood": 120}
        truth_teller = UnlockTech(tech="unlock_truth_teller")
        truth_teller_research = ResearchSkill(self, cost, "TruthTellerPIcon", truth_teller, time_requirement=30,
                                        flag="unlock_truth_teller", animate="produce")
        self.skill_manager.add(truth_teller_research)
        self.skill_panel.replace("TruthTellerPIcon", truth_teller_research, describe="研究-热力学&用时:30s&允许机械工厂训"
                                                                            "练\"真理叙说者\"",
                                 key="X", line=3, column=1, mouse=False)

        self.unit_panel["unit_label"] = ("建筑", "大型单位")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "研究院"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "研究院"
        self.unit_panel["unit_icon"] = "instituteIcon"

        self.if_build_complete = False

    def finish_build(self):
        super().finish_build()
        self.if_build_complete = True
        TechTree.add_level("institute_count", self.team, 1)

    def clear(self):
        if self.if_build_complete:
            TechTree.add_level("institute_count", self.team, -1)
        super().clear()

