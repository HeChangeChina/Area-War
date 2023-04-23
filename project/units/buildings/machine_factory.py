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


class MachineFactory(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/MachineFactory", "MachineFactory", pygame.Rect(x, y, 250, 250),
                         unit_height_c=248,
                         attribute_manager=AttributeManager(max_health=950, max_magic=0, magic_armor=0,
                                                            armor_tech=("masonry", "masonry"), physical_armor=7),
                         population_produce=0)
        self.flag.add_flag(["machine_factory", "production_unit"])
        self.volume = 120
        self.cost = {"gold": 140, "wood": 220}

        cost = {"gold": 130, "wood": 150}
        produce_fly_machine = ProduceSkill(self, "FlyMachine", "FlyMachineIcon", cost, 3, 32, animate="produce",
                                         flag="FlyMachine")
        self.skill_manager.add(produce_fly_machine)
        self.skill_panel.replace("FlyMachinePIcon", produce_fly_machine, describe="训练-飞行机器&用时:32s&粗糙而又简陋的工"
                                                                               "艺，但至少，它飞起来了",
                                 key="Q", line=3, column=0, mouse=False)

        cost = {"gold": 350, "wood": 450}
        produce_truth_teller = ProduceSkill(self, "TruthTeller", "TruthTellerIcon", cost, 6, 70, animate="produce",
                                            flag="TruthTeller", tech_require="unlock_truth_teller", tech_mode="have")
        self.skill_manager.add(produce_truth_teller)
        self.skill_panel.replace("TruthTellerPIcon", produce_truth_teller, describe="训练-真理叙说者&用时:70s&这种缓慢的飞"
                                                                                   "行机器一旦接触到敌方的防线，就可以对它"
                                                                                   "们造成毁灭性的打击",
                                 key="W", line=3, column=1, mouse=False)

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=120))
        self.behavior_manager.add(ProduceListShower())

        self.unit_panel["unit_label"] = ("建筑", "大型单位")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "机械工厂"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "机械工厂"
        self.unit_panel["unit_icon"] = "MachineFactoryIcon"

        self.if_build_complete = False

    def finish_build(self):
        super().finish_build()
        self.if_build_complete = True
        TechTree.add_level("machine_factory_count", self.team, 1)

    def clear(self):
        if self.if_build_complete:
            TechTree.add_level("machine_factory_count", self.team, -1)
        super().clear()
