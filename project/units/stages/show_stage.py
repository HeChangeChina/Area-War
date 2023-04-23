from console.button import Button
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
from auxiliary_tools.tech_tree import TechTree
from unit_tools.team_manager import TeamManager
import random


class ShowStage(PlayStage):
    def __init__(self, father_surface):
        super().__init__(father_surface, 12000)
        self.if_win = False
        self.self_base = None
        self.enemy_base = None
        self.wave_enemy = list()

    def left_enemy(self, data):
        self.print_font.change_text("防御敌人(生产加速:5倍，资源倍数:5倍)")
        TechTree.set_level("rifle", 1, 1)
        for i in range(1):
            enemy = Knight(-2800 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(2):
            enemy = Soldier(-2700 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(3):
            enemy = Musketeer(-3000 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(2):
            enemy = Minister(-3000 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(2):
            enemy = FlyMachine(-3800 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(1):
            enemy = TruthTeller(-3000 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in self.wave_enemy:
            i.controller.use_skill(["skill", "attack"], (0, 0))

    def right_enemy(self, data):
        self.print_font.change_text("防御敌人(生产加速:5倍，资源倍数:5倍)")
        TechTree.set_level("array", 1, 1)
        TechTree.set_level("master_ranger", 1, 1)
        TechTree.set_level("rifle", 1, 1)
        TechTree.set_level("envenomed", 1, 1)
        for i in range(2):
            enemy = Ranger(2400 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(2):
            enemy = Soldier(1800 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(1):
            enemy = Musketeer(2000 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in range(2):
            enemy = Minister(2000 + 50 * i, 300)
            enemy.change_team(1)
            self.create_unit(enemy)
            self.wave_enemy.append(enemy)

        for i in self.wave_enemy:
            i.controller.use_skill(["skill", "attack"], (0, 0))

    def add_exp(self, data):
        for i in self.unit_list:
            if i.flag.contain_flag("hero"):
                i.attribute_manager.add_exp(300)

    def update(self):
        super().update()
        if len(self.wave_enemy) == 0:
            self.print_font.change_text("无任务目标(生产加速:5倍，资源倍数:5倍)")
        else:
            self.print_font.change_text("防御敌人(剩余:%s)(生产加速:5倍，资源倍数:5倍)" % len(self.wave_enemy))

    def start(self):
        self.print_font.change_text("无任务目标(生产加速:5倍，资源倍数:5倍)")
        self.set_camera_limit_x(-4000, 5000)

        ResourcesManager.add_resources("gold", 999999, 1)
        ResourcesManager.add_resources("wood", 999999, 1)

        ResourcesManager.add_resources("gold", 250, 0)
        ResourcesManager.add_resources("wood", 160, 0)

        TeamManager.alliance(0, 3)

        left_enemy_button = Button(1700, 100, "触发左进攻波次(大)", "left_enemy")
        right_enemy_button = Button(1700, 200, "触发右进攻波次(小)", "right_enemy")
        exp_button = Button(1700, 300, "给予英雄经验(300)", "add_exp")
        self.add(left_enemy_button, index=40, z=0)
        self.add(right_enemy_button, index=40, z=0)
        self.add(exp_button, index=40, z=0)
        self.message_require("left_enemy", self.left_enemy)
        self.message_require("right_enemy", self.right_enemy)
        self.message_require("ad_exp", self.add_exp)

        for i in range(2):
            tree = Tree(-700 + 100 * i, 0)
            self.create_unit(tree)

        for i in range(1):
            tree = Tree(600 + 100 * i, 0)
            self.create_unit(tree)

        for i in range(3):
            tree = Tree(-1150 + 100 * i, 0)
            self.create_unit(tree)

        for i in range(3):
            worker = Worker(i * 50, 300)
            self.create_unit(worker)
        self.self_base = Base(0, 0)
        self.create_unit(self.self_base)

        tower = Bartizan(1000, 0)
        tower.change_team(3)
        self.create_unit(tower)

        for i in range(1):
            ranger = Ranger(1000 + 50 * i, 300)
            ranger.change_team(3)
            self.create_unit(ranger)

        soldier = Soldier(1100, 300)
        soldier.change_team(3)
        self.create_unit(soldier)
