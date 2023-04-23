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


class TrainingGround(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/TrainingGround", "TrainingGround", pygame.Rect(x, y, 250, 200),
                         unit_height_c=198,
                         attribute_manager=AttributeManager(max_health=900, max_magic=0, magic_armor=0,
                                                            armor_tech=("masonry", "masonry"), physical_armor=7),
                         population_produce=0)
        self.flag.add_flag(["training_ground", "production_unit"])
        self.volume = 100
        self.cost = {"gold": 180, "wood": 160}

        self.behavior_manager.add(HMBar(width=0.8))
        self.behavior_manager.add(Shadow(shadow_size=100))
        self.behavior_manager.add(ProduceListShower())

        cost = {"gold": 120, "wood": 35}
        produce_soldier = ProduceSkill(self, "soldier", "soldierIcon", cost, 2, 21, animate="produce", flag="soldier")
        self.skill_manager.add(produce_soldier)
        self.skill_panel.replace("soldierPIcon", produce_soldier, describe="训练-士兵&用时:21s&基础的作战单位，可以习得技能\"列阵\"",
                                 key="Q", line=3, column=0, mouse=False)

        cost = {"gold": 90, "wood": 65}
        produce_ranger = ProduceSkill(self, "ranger", "rangerIcon", cost, 2, 18, animate="produce", flag="ranger")
        self.skill_manager.add(produce_ranger)
        self.skill_panel.replace("rangerPIcon", produce_ranger, describe="训练-游侠&用时:18s&游侠可以快速穿梭于战场之"
                                                                         "间，她们箭无虚发，百发百中(可以攻击空中目标)",
                                 key="W", line=3, column=1, mouse=False)

        cost = {"gold": 170, "wood": 50}
        produce_musketeer = ProduceSkill(self, "musketeer", "musketeerIcon", cost, 3, 26, animate="produce",
                                         flag="musketeer", tech_require="crafter_house_count", tech_mode="have")
        self.skill_manager.add(produce_musketeer)
        self.skill_panel.replace("musketeerPIcon", produce_musketeer, describe="训练-火枪手&用时:26s&需要:工匠铺&瞄准，射击，这就是火枪手"
                                                                               "对敌的手段，精制的弹丸能对他们的敌人造成高额的"
                                                                               "物理伤害(可以攻击空中目标)",
                                 key="E", line=3, column=2, mouse=False)

        cost = {"gold": 450, "wood": 300}
        produce_knight = ProduceSkill(self, "knight", "knightIcon", cost, 6, 5, animate="produce",
                                      flag="knight", tech_require="unlock_knight", tech_mode="not have")
        self.skill_manager.add(produce_knight)
        self.skill_panel.replace("knightPIcon", produce_knight, describe="训练-\"大块头\"&用时:65s&这些包裹的严严实实"
                                                                         "的铁罐头们是敌人的噩梦，他们的长枪可以轻而易"
                                                                         "举的撕裂敌人的防线，拥有技能\"战吼\"",
                                 key="R", line=3, column=3, mouse=False)

        cost = {"gold": 170, "wood": 130}
        unlock_master_ranger = UnlockTech(tech="array")
        unlock_array = ResearchSkill(self, cost, "arrayIcon", unlock_master_ranger, time_requirement=55,
                                     flag="unlock_array", tech_require="array", tech_mode="not have")
        self.skill_manager.add(unlock_array)
        self.skill_panel.replace("arrayIcon", unlock_array, describe="研究-列阵&用时:55s&士兵的周围每存在一个士兵，"
                                                                     "造成的伤害提高6%，受到的伤害减少6%，最多叠加5次。",
                                 key="Z", line=2, column=0, mouse=False)

        cost = {"gold": 150, "wood": 150}
        unlock_master_ranger = UnlockTech(tech="master_ranger")
        unlock_ms = ResearchSkill(self, cost, "MasterRangerIcon", unlock_master_ranger, time_requirement=45,
                                  flag="unlock_master_ranger", tech_require="master_ranger", tech_mode="not have")
        self.skill_manager.add(unlock_ms)
        self.skill_panel.replace("MasterRangerIcon", unlock_ms, describe="研究-大师级游侠训练&用时:45s&游侠的攻击距离增加150",
                                 key="X", line=2, column=1, mouse=False)

        cost = {"gold": 100, "wood": 100}
        unlock_roar = UnlockTech(tech="roar")
        unlock_roars = ResearchSkill(self, cost, "roarIcon", unlock_roar, time_requirement=37,
                                  flag="unlock_roar", tech_require="roar", tech_mode="not have")
        self.skill_manager.add(unlock_roars)
        self.skill_panel.replace("roarIcon", unlock_roars, describe="研究-战吼&用时:37s&\"大块头\"可以使周围的己方"
                                                                    "单位造成伤害提高25%",
                                 key="C", line=2, column=3, mouse=False)

        self.unit_panel["unit_label"] = ("建筑", "大型单位")
        self.unit_panel["armor_name"] = ("砖石墙面", "砖石墙面")
        self.unit_panel["name"] = "训练场"
        self.unit_panel["base_info"] = 15
        self.unit_panel["title"] = "训练场"
        self.unit_panel["unit_icon"] = "TrainingGroundIcon"

        self.if_build_complete = False

    def finish_build(self):
        super().finish_build()
        self.if_build_complete = True
        TechTree.add_level("training_ground_count", self.team, 1)

    def clear(self):
        if self.if_build_complete:
            TechTree.add_level("training_ground_count", self.team, -1)
        super().clear()
