from units.stages.play_stage import PlayStage
from units.movable_units.slim import Slim
from units.movable_units.worker import Worker
from units.buildings.base import Base
from units.movable_units.lin import Lin
from units.movable_units.ranger import Ranger
from units.movable_units.soldier import Soldier
from units.movable_units.musketeer import Musketeer
from units.movable_units.knight import Knight
from units.movable_units.minister import Minister
from units.movable_units.master import Master
from units.movable_units.fly_machine import FlyMachine
from units.movable_units.truth_teller import TruthTeller
from units.buildings.tree import Tree
from units.buildings.hero_altar import HeroAltar
from units.buildings.test_building import TestBuilding
from units.buildings.training_ground import TrainingGround
from units.buildings.residential_building import ResidentialBuilding
from units.buildings.storehouse import Storehouse
from units.buildings.institute import Institute
from units.buildings.crafter_house import CrafterHouse
from units.buildings.bonfire import Bonfire
from units.buildings.bartizan import Bartizan
from units.buildings.machine_factory import MachineFactory
from units.buildings.magic_college import MagicCollege
from auxiliary_tools.resources_manager import ResourcesManager
from unit_tools.team_manager import TeamManager
import random


class BattleStage(PlayStage):
    def __init__(self, father_surface):
        super().__init__(father_surface, 12000)
        self.if_win = False
        self.self_base = None
        self.enemy_base = None

    def start(self):
        self.set_camera_limit_x(-4000, 5000)

        ResourcesManager.add_resources("gold", 999999, 1)
        ResourcesManager.add_resources("wood", 999999, 1)

        ResourcesManager.add_resources("gold", 300, 0)
        ResourcesManager.add_resources("wood", 160, 0)

        TeamManager.alliance(0, 3)

        self.print_font.change_text("任务目标：摧毁位于右侧的敌方基地(己方基地不能被摧毁)")
        # self.move_camera((2500, 0))
        # 创建初始基地
        for i in range(3):
            worker = Worker(-2000 + i * 50, 300)
            self.create_unit(worker)
        self.self_base = Base(-2000, 0)
        self.create_unit(self.self_base)

        worker = Worker(2000, 300)
        self.create_unit(worker)

        # 创建基地旁的树林
        for i in range(2):
            tree = Tree(-2550 + i * 100, 0)
            self.create_unit(tree)

        for i in range(4):
            tree = Tree(-1000 + 100 * i, 0)
            self.create_unit(tree)

        for i in range(3):
            tree = Tree(-3950 + 100 * i, 0)
            self.create_unit(tree)

        for i in range(3):
            tree = Tree(-3500 + 100 * i, 0)
            self.create_unit(tree)

        # 创建左侧的史莱姆
        for i in range(8):
            slim = Slim(-4000 + i * 50, 300)
            slim.change_team(1)
            self.create_unit(slim)
            slim.controller.use_skill(["skill", "patrol"], (-3600 + random.random() * 200, 0))

        # 创建右侧友方防御塔
        tower = Bartizan(-500, 0)
        tower.change_team(3)
        self.create_unit(tower)

        for i in range(1):
            ranger = Ranger(-600 + 50 * i, 300)
            ranger.change_team(3)
            self.create_unit(ranger)

        soldier = Soldier(-450, 300)
        soldier.change_team(3)
        self.create_unit(soldier)

        # 创建右侧的敌方基地
        for i in range(1):
            tower = Bartizan(3000 + i * 100, 0)
            tower.change_team(2)
            self.create_unit(tower)

        for i in range(1):
            soldier = Soldier(3000 + i * 60, 0)
            soldier.change_team(2)
            self.create_unit(soldier)

        for i in range(2):
            ranger = Ranger(3300 + i * 60, 0)
            ranger.change_team(2)
            self.create_unit(ranger)

        training_ground = TrainingGround(3300, 0)
        training_ground.change_team(2)
        self.create_unit(training_ground)
        tree_list = list()
        for i in range(2):
            tree = Tree(3550 + 100 * i, 0)
            tree_list.append(tree)
            self.create_unit(tree)

        storehouse = Storehouse(4000, 0)
        storehouse.change_team(2)
        self.create_unit(storehouse)

        bonfire = Bonfire(3850, 0)
        bonfire.change_team(2)
        self.create_unit(bonfire)

        for i in range(3):
            worker = Worker(4000 + i * 40, 300)
            worker.change_team(2)
            worker.controller.use_skill(["collect", "skill"], random.choice(tree_list))
            self.create_unit(worker)

        worker = Worker(4400, 300)
        worker.change_team(2)
        self.create_unit(worker)

        for i in range(2):
            tower = Bartizan(4200 + i * 100, 0)
            tower.change_team(2)
            self.create_unit(tower)

        for i in range(2):
            soldier = Soldier(4100 + i * 60, 0)
            soldier.change_team(2)
            self.create_unit(soldier)

        for i in range(1):
            minister = Minister(4500 + i * 60, 0)
            minister.change_team(2)
            self.create_unit(minister)

        for i in range(1):
            master = Master(4500 + i * 60, 0)
            master.change_team(2)
            self.create_unit(master)

        bonfire = Bonfire(4700, 0)
        bonfire.change_team(2)
        self.create_unit(bonfire)

        institute = Institute(4500, 0)
        institute.change_team(2)
        self.create_unit(institute)

        for i in range(3):
            tower = Bartizan(5100 + i * 100, 0)
            tower.change_team(2)
            self.create_unit(tower)

        knight = Knight(5100, 0)
        knight.change_team(2)
        self.create_unit(knight)

        truth_teller = TruthTeller(5400, 0)
        truth_teller.change_team(2)
        self.create_unit(truth_teller)

        for i in range(2):
            fly_machine = FlyMachine(5100 + i * 130, 0)
            fly_machine.change_team(2)
            self.create_unit(fly_machine)

        for i in range(2):
            minister = Minister(5500 + i * 60, 0)
            minister.change_team(2)
            self.create_unit(minister)

        for i in range(2):
            worker = Worker(5400 + i * 40, 300)
            worker.change_team(2)
            self.create_unit(worker)

        self.enemy_base = Base(5400, 0)
        self.enemy_base.change_team(2)
        self.create_unit(self.enemy_base)

        residential = ResidentialBuilding(5900, 0)
        residential.change_team(2)
        self.create_unit(residential)




