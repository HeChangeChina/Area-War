from units.movable_unit import MovableUnit
from unit_tools.attribute_manager import AttributeManager
from units.skills.build import BuildSkill
from units.skills.repair import RepairSkill
from units.skills.collect import CollectSkill
from units.behaviors.health_magic_bar import HMBar
from units.behaviors.shadow import Shadow
import pygame


class Worker(MovableUnit):
    def __init__(self, x, y):
        attribute_manager = AttributeManager(0, max_health=150, max_magic=0, magic_armor=0, physical_armor=4,
                                             armor_tech=("human_armor", "human_armor"), armor_level_add=(1, 0))
        super().__init__("./data/img/units/movable/worker", "worker", pygame.Rect(x, y, 60, 60), unit_height_c=55,
                         attribute_manager=attribute_manager, population_cost=1)
        self.flag.add_flag(["worker", "land_force", "human"])

        self.behavior_manager.add(HMBar(width=0.7))
        self.behavior_manager.add(Shadow(c_x=0))

        build_training_ground = BuildSkill(self, "TrainingGround", 198, 250, 0, {"gold": 180, "wood": 160},
                                           build_time=35)
        build_residential_building = BuildSkill(self, "ResidentialBuilding", 98, 100, 0, {"gold": 130, "wood": 80},
                                                build_time=18)
        build_storehouse = BuildSkill(self, "storehouse", 98, 150, 0, {"gold": 60, "wood": 80},
                                      build_time=14)
        build_institute = BuildSkill(self, "institute", 238, 300, 0, {"gold": 270, "wood": 140},
                                     build_time=50, tech_require="crafter_house_count", tech_mode="have")
        build_crafter_house = BuildSkill(self, "CrafterHouse", 78, 150, 0, {"gold": 120, "wood": 90},
                                         build_time=21)
        build_hero_altar = BuildSkill(self, "HeroAltar", 398, 150, 0, {"gold": 80, "wood": 130},
                                      build_time=30, tech_require="training_ground_count", tech_mode="have")
        build_bartizan = BuildSkill(self, "bartizan", 248, 100, 0, {"gold": 90, "wood": 110},
                                    build_time=27)
        build_machine_factory = BuildSkill(self, "MachineFactory", 248, 250, 0, {"gold": 140, "wood": 220},
                                           build_time=27, tech_require="institute_count", tech_mode="have")
        build_magic_college = BuildSkill(self, "MagicCollege", 248, 250, 0, {"gold": 250, "wood": 120},
                                         build_time=27, tech_require="institute_count", tech_mode="have")
        build_bonfire = BuildSkill(self, "bonfire", 65, 50, 1, {"gold": 20, "wood": 110},
                                   build_time=5)
        repair_skill = RepairSkill(self, animate="repair")
        collect_skill = CollectSkill(self, "CuttingTree")

        self.skill_manager.add(build_training_ground)
        self.skill_manager.add(build_residential_building)
        self.skill_manager.add(build_storehouse)
        self.skill_manager.add(build_institute)
        self.skill_manager.add(build_crafter_house)
        self.skill_manager.add(build_hero_altar)
        self.skill_manager.add(build_bartizan)
        self.skill_manager.add(build_machine_factory)
        self.skill_manager.add(build_magic_college)
        self.skill_manager.add(build_bonfire)
        self.skill_manager.add(repair_skill)
        self.skill_manager.add(collect_skill)

        self.skill_panel.replace("repairI", describe="维修&消耗资源，维修友方或己方机械单位或者建筑，每秒回复目标15点血量",
                                 line=1, column=0, skill=repair_skill, key="R", panel="defeat", mouse=True)
        self.skill_panel.replace("buildI", None, describe="普通建造面板&打开普通建筑建造面板",
                                 key="B", line=3, column=0, mouse=False, panel="defeat", panel_to="build_000")
        self.skill_panel.replace("build2I", None, describe="特殊建造面板&打开特殊建筑建造面板&(特殊建筑可以于普通建筑重叠建造)",
                                 key="V", line=3, column=1, mouse=False, panel="defeat", panel_to="build_001")
        self.skill_panel.replace("collectI", collect_skill, describe="采集/送回资源&选择资源点或存放点，持续采集周围的同类资"
                                                                     "源或当前携带资源，直至找不到存放点或无同类资源",
                                 key="C", line=1, column=1, mouse=True, panel="defeat")
        self.skill_panel.replace("SkillCancel", None, describe="返回&返回主菜单",
                                 key="Q", line=3, column=4, mouse=False, panel="build_000", panel_to="defeat")
        self.skill_panel.replace("SkillCancel", None, describe="返回&返回主菜单",
                                 key="Q", line=3, column=4, mouse=False, panel="build_001", panel_to="defeat")

        self.skill_panel.replace("TrainingGroundPIcon", build_training_ground, describe="建造-训练场&用时:35s&训练场可以训练基本"
                                                                                        "的作战单位，包括士兵，游侠，在升"
                                                                                        "级科技后，还可以训练火枪手，\"大块头\"",
                                 key="B", line=0, column=0, mouse=False, panel="build_000")
        self.skill_panel.replace("ResidentialBuildingPIcon", build_residential_building, describe="建造-居民楼&用时:18s&居民楼"
                                                                                                  "提供8点人口，并可以定期产"
                                                                                                  "生金币税收，是重要的经济来源",
                                 key="R", line=0, column=1, mouse=False, panel="build_000")

        self.skill_panel.replace("storehousePIcon", build_storehouse, describe="建造-仓库&用时:14s&矮人工匠采集的资源"
                                                                               "还可以送还至仓库，而非基地",
                                 key="S", line=0, column=2, mouse=False, panel="build_000")

        self.skill_panel.replace("institutePIcon", build_institute, describe="建造-研究院&用时:50s&需要:工匠铺&研究院可以研究各项高"
                                                                             "级的科技，以解锁或升级更多的建筑和单位",
                                 key="H", line=2, column=0, mouse=False, panel="build_000")

        self.skill_panel.replace("CrafterHousePIcon", build_crafter_house, describe="建造-工匠铺&用时:21s&工匠铺可以升级单"
                                                                                    "位的武器与护甲等级，并且可以研究初等的科技",
                                 key="E", line=1, column=0, mouse=False, panel="build_000")

        self.skill_panel.replace("HeroAltarPIcon", build_hero_altar, describe="建造-英雄祭坛&用时:30s&需要:训练场&英雄祭坛可以"
                                                                              "召唤不同的英雄(现只有\"琳\")，英雄只能召唤一次，但"
                                                                              "可以消耗资源不断复活",
                                 key="V", line=1, column=1, mouse=False, panel="build_000")

        self.skill_panel.replace("bartizanPIcon", build_bartizan, describe="建造-箭塔&用时:27s&基础的防御建筑，对来犯"
                                                                           "敌人射出弩箭(可以攻击空中目标)",
                                 key="T", line=0, column=3, mouse=False, panel="build_000")

        self.skill_panel.replace("MachineFactoryPIcon", build_machine_factory, describe="建造-机械工厂&用时:27s&需要:研究院&"
                                                                                        "这个工厂可以源源不断地产出各种无人"
                                                                                        "机械，如果你的资源充足的话",
                                 key="G", line=2, column=1, mouse=False, panel="build_000")

        self.skill_panel.replace("MagicCollegePIcon", build_magic_college, describe="建造-魔法学院&用时:27s&需要:研究院&"
                                                                                    "魔法学院可以训练牧师和魔法师，他们是"
                                                                                    "战场上的一大助力",
                                 key="F", line=2, column=2, mouse=False, panel="build_000")

        self.skill_panel.replace("bonfirePIcon", build_bonfire, describe="搭建-篝火&用时:5s&篝火可以提高周"
                                                                         "围的友方人类单位的生命回复速度",
                                 key="F", line=0, column=0, mouse=False, panel="build_001")

        self.cost = {"gold": 80, "wood": 0}
        self.exp_produce = 5

        self.unit_panel["unit_label"] = ("小型单位", "轻型单位", "人类")
        self.unit_panel["armor_name"] = ("矮人布衣", "矮人布衣")
        self.unit_panel["name"] = "矮人工匠"
        self.unit_panel["unit_icon"] = "workerIcon"
        self.unit_panel["title"] = "不是来自铁炉堡的矮人"
        self.unit_panel["text_y"] = 110

        self.visual_field = 450
        self.radar_range = 1200

    def update_60(self):
        resource_amount = self.attribute_manager.get_attribute("resource_carry")
        if resource_amount is not None:
            self.unit_panel["text"] = "资源携带量:%.0f" % resource_amount[1]
