from units.building import Building
from units.behaviors.shadow import Shadow
from units.behaviors.health_magic_bar import HMBar
from units.skills.research import ResearchSkill
from units.effect.mixed_effect import MixedEffect
from units.effect.add_tech_level import AddTechLevel
from units.effect.unlock_tech import UnlockTech
from unit_tools.attribute_manager import AttributeManager
from units.behaviors.produce_lists_shower import ProduceListShower
from auxiliary_tools.tech_tree import TechTree
import pygame


class CrafterHouse(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/CrafterHouse", "CrafterHouse", pygame.Rect(x, y, 150, 80),
                         unit_height_c=78,
                         attribute_manager=AttributeManager(max_health=650, max_magic=0, magic_armor=0,
                                                            armor_tech=("masonry", "masonry"), physical_armor=5),
                         population_produce=0)
        self.flag.add_flag(["crafter_house"])
        self.volume = 70
        self.cost = {"gold": 120, "wood": 90}

        cost = {"gold": 100, "wood": 100}
        level_1 = UnlockTech(tech="human_armor_001")
        human_armor_001 = AddTechLevel(tech="human_armor")
        mixed_level_001 = MixedEffect(effects=[level_1, human_armor_001])
        add_armor_level_01 = ResearchSkill(self, cost, "HumanArmorLEVEL1", mixed_level_001, time_requirement=60,
                                           flag="human_armor_001", tech_require="human_armor_001", tech_mode="not have",
                                           animate="produce")
        self.skill_manager.add(add_armor_level_01)
        self.skill_panel.replace("HumanArmorLEVEL1", add_armor_level_01, describe="研究-人类护甲等级1&用时:60s&提升所有己"
                                                                                  "方人类单位的护甲等级",
                                 key="E", line=3, column=0, mouse=False)

        cost = {"gold": 100, "wood": 100}
        level_1 = UnlockTech(tech="human_weapon_001")
        human_weapon_001 = AddTechLevel(tech="human_weapon")
        mixed_level_001 = MixedEffect(effects=[level_1, human_weapon_001])
        add_weapon_level_01 = ResearchSkill(self, cost, "HumanWeaponLEVEL1", mixed_level_001, time_requirement=60,
                                            flag="human_weapon_001", tech_require="human_weapon_001",
                                            tech_mode="not have", animate="produce")
        self.skill_manager.add(add_weapon_level_01)
        self.skill_panel.replace("HumanWeaponLEVEL1", add_weapon_level_01, describe="研究-人类武器等级1&用时:60s&提升所有己"
                                                                                    "方人类单位的武器等级",
                                 key="W", line=3, column=1, mouse=False)

        cost = {"gold": 175, "wood": 175}
        level_2 = UnlockTech(tech="human_armor_002")
        human_armor_002 = AddTechLevel(tech="human_armor")
        mixed_level_002 = MixedEffect(effects=[level_2, human_armor_002])
        add_armor_level_02 = ResearchSkill(self, cost, "HumanArmorLEVEL2", mixed_level_002, time_requirement=90,
                                           flag="human_armor_002",
                                           tech_require=("human_armor_002", "institute_count", "human_armor_001"),
                                           tech_mode=("not have", "have", "have"), animate="produce")
        self.skill_manager.add(add_armor_level_02)
        self.skill_panel.replace("HumanArmorLEVEL2", add_armor_level_02, describe="研究-人类护甲等级2&用时:90s&需要:研"
                                                                                  "究院，人类护甲等级1&提升所有己"
                                                                                  "方人类单位的护甲等级",
                                 key="E", line=2, column=0, mouse=False)

        cost = {"gold": 175, "wood": 175}
        level_2 = UnlockTech(tech="human_weapon_002")
        human_weapon_002 = AddTechLevel(tech="human_weapon")
        mixed_level_002 = MixedEffect(effects=[level_2, human_weapon_002])
        add_weapon_level_02 = ResearchSkill(self, cost, "HumanWeaponLEVEL2", mixed_level_002, time_requirement=90,
                                            flag="human_weapon_002",
                                            tech_require=("human_weapon_002", "institute_count", "human_weapon_001"),
                                            tech_mode=("not have", "have", "have"), animate="produce")
        self.skill_manager.add(add_weapon_level_02)
        self.skill_panel.replace("HumanWeaponLEVEL2", add_weapon_level_02, describe="研究-人类武器等级2&用时:90s&需要:研"
                                                                                    "究院，人类武器等级1&提升所有己"
                                                                                    "方人类单位的武器等级",
                                 key="W", line=2, column=1, mouse=False)

        cost = {"gold": 250, "wood": 250}
        level_3 = UnlockTech(tech="human_armor_003")
        human_armor_003 = AddTechLevel(tech="human_armor")
        mixed_level_003 = MixedEffect(effects=[level_3, human_armor_003])
        add_armor_level_03 = ResearchSkill(self, cost, "HumanArmorLEVEL3", mixed_level_003, time_requirement=120,
                                           flag="human_armor_003",
                                           tech_require=("human_armor_003", "machine_factory_count",
                                                         "magic_college_count", "human_armor_002"),
                                           tech_mode=("not have", "have", "have", "have"), animate="produce")
        self.skill_manager.add(add_armor_level_03)
        self.skill_panel.replace("HumanArmorLEVEL3", add_armor_level_03, describe="研究-人类护甲等级3&用时:120s&需要:机"
                                                                                  "械工厂，魔法学院，人类护甲等级2&提升所有己"
                                                                                  "方人类单位的护甲等级",
                                 key="E", line=1, column=0, mouse=False)

        cost = {"gold": 250, "wood": 250}
        level_3 = UnlockTech(tech="human_weapon_003")
        human_weapon_003 = AddTechLevel(tech="human_weapon")
        mixed_level_003 = MixedEffect(effects=[level_3, human_weapon_003])
        add_weapon_level_03 = ResearchSkill(self, cost, "HumanWeaponLEVEL3", mixed_level_003, time_requirement=120,
                                            flag="human_weapon_003",
                                            tech_require=("human_weapon_003", "machine_factory_count",
                                                          "magic_college_count", "human_weapon_002"),
                                            tech_mode=("not have", "have", "have", "have"), animate="produce")
        self.skill_manager.add(add_weapon_level_03)
        self.skill_panel.replace("HumanWeaponLEVEL2", add_weapon_level_03, describe="研究-人类武器等级3&用时:120s&需要:机"
                                                                                    "械工厂，魔法学院，人类武器等级2&提升所有己"
                                                                                    "方人类单位的武器等级",
                                 key="W", line=1, column=1, mouse=False)

        cost = {"gold": 125, "wood": 125}
        rifle = UnlockTech(tech="rifle")
        rifle_research = ResearchSkill(self, cost, "rifleIcon", rifle, time_requirement=55,
                                       flag="rifle", animate="produce")
        self.skill_manager.add(rifle_research)
        self.skill_panel.replace("rifleIcon", rifle_research, describe="研究-膛线改良&用时:55s&火枪手的攻击间隔减少30%",
                                 key="Z", line=3, column=2, mouse=False)

        cost = {"gold": 150, "wood": 150}
        envenomed = UnlockTech(tech="envenomed")
        envenomed_research = ResearchSkill(self, cost, "envenomedIcon", envenomed, time_requirement=50,
                                           flag="envenomed", animate="produce")
        self.skill_manager.add(envenomed_research)
        self.skill_panel.replace("envenomedIcon", envenomed_research, describe="研究-淬毒武器&用时:50s&游侠的攻击使敌方"
                                                                               "中毒，降低目标的防御力，并使目标持续受到"
                                                                               "真实伤害",
                                 key="X", line=3, column=3, mouse=False)

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=70))
        self.behavior_manager.add(ProduceListShower())

        self.unit_panel["unit_label"] = ("建筑", "小型单位")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "工匠铺"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "工匠铺"
        self.unit_panel["unit_icon"] = "CrafterHouseIcon"

        self.if_build_complete = False

    def finish_build(self):
        super().finish_build()
        self.if_build_complete = True
        TechTree.add_level("crafter_house_count", self.team, 1)

    def clear(self):
        if self.if_build_complete:
            TechTree.add_level("crafter_house_count", self.team, -1)
        super().clear()
