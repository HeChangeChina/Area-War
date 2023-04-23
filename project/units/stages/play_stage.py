import pygame
import math
from display.stage import Stage
from auxiliary_tools.message_manager import MessageManager
from auxiliary_tools.resources_manager import ResourcesManager
from auxiliary_tools.tech_tree import TechTree
from auxiliary_tools.circle import Circle
from auxiliary_tools.key_listener import KeyListener
from units.ground import Ground
from units.fog import Fog
from units.movable_units.slim import Slim
from units.movable_units.worker import Worker
from units.buildings.base import Base
from units.movable_units.lin import Lin
from units.movable_units.ranger import Ranger
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
from units.backgorund.background import Background
from units.ground_drawer import GroundDrawer
from units.indicator_drawer import IndicatorDrawer
from units.behaviors.preselection import Preselection
from display.normal_display import NormalDisplay
from unit_tools.projection_drawer import ProjectionDrawer
from unit_tools.team_manager import TeamManager
from display.font import Font
from display.cursor import Cursor
from console.console import Console
from console.stop_button import StopButton
from random import random


class PlayStage(Stage):
    def __init__(self, father_surface, length=20000):
        super().__init__(0, 0, 1920, 1080, father_surface, draw_on_father=True)

        self.stop_button = StopButton()
        self.add(self.stop_button, z=0, index=50)

        TeamManager.reset_teams()
        TeamManager.player_team = 0
        ResourcesManager.reset()
        TechTree.reset_tech()

        TeamManager.alliance(0, 9)
        TeamManager.alliance(1, 9)
        TeamManager.alliance(2, 9)
        TeamManager.alliance(3, 9)
        TeamManager.alliance(4, 9)
        TeamManager.alliance(5, 9)

        self.background = NormalDisplay("./data/img/background", "sky", pygame.Rect(0, 0, 1920, 800))
        self.add(self.background, index=-200, z=0)
        self.camera_shifting = [-100, 0]
        self.ground = Ground(length)
        self.projection_drawer = ProjectionDrawer()
        self.add(self.ground, -10)
        self.ground_drawer = GroundDrawer(length)
        self.add(self.ground_drawer, -9)
        self.set_sky_box((115, 190, 230))
        self.indicator_drawer = IndicatorDrawer()
        self.console = Console()
        self.add(self.console, 50, 0)
        self.add_background(length)
        self.fog = Fog()
        self.add(self.fog, index=40, z=0)
        self.set_camera_limit_x(-length / 2, length / 2)
        self.length = length

        self.unit_list = list()
        self.cloud_list = list()
        for i in range(length // 800 + 1):
            left = i * 800 + random() * 800 - 800 - length / 2
            top = 100 + random() * 250
            speed = 9 + random() * 7
            last_time = 50 + random() * 30
            cloud = Background("cloud", "grassland", 0, pygame.Rect(left, top, 400, 200), speed, last_time, shadow_size=150,
                               shadow_c=30)
            self.add(cloud, z=1, index=-101)
            self.cloud_list.append(cloud)

        self.mouse_down_c = [0, 0]
        self.mouse_drag = False
        self.mouse_drag_units = list()
        self.mouse_double_click_record = [None, 0]
        self.skill_aiming = False
        self.aiming_sight = None
        self.aiming_skill = None
        self.aiming_skill_target_mode = None
        self.aiming_prevent_up = 0

        self.frame = Font("60", 25, pygame.Rect(10, 10, 300, 50))
        self.print_font = Font("无任务目标", 25, pygame.Rect(150, 10, 300, 50))
        self.add(self.frame, index=99, z=0)
        self.add(self.print_font, index=99, z=0)
        self.cursor = Cursor()
        self.add(self.cursor, index=100, z=0)

        self.if_pressed_right = False

        self.message_require("print_on_screen", self.print_data)
        self.message_require("update_15", self.radar_update)
        self.message_require("add_display", self.message_add)
        self.message_require("search_range", self.search_range)
        self.message_require("create_bullet", self.create_bullet)
        self.message_require("create_trajectory", self.create_trajectory)
        self.message_require("create_special_effect", self.create_special_effect)
        self.message_require("unit_die", self.unit_die)
        self.message_require("frame", self.set_frame)
        self.message_require("skill_aim", self.skill_aim)
        self.message_require("create_unit", self.create_unit)
        self.message_require("focus_on", self.focus)

        self.sky_box = (-1, 0, 0)

        self.start()

    def start(self):
        ResourcesManager.add_resources("gold", 100000, 0)
        ResourcesManager.add_resources("wood", 100000, 0)
        test_list = list()
        for i in range(5):
            slim = Worker(300 + i * 50, 300)
            self.create_unit(slim)
            test_list.append(slim)
        for i in range(15):
            slim = Slim(1500 + i * 40, 300)
            slim.change_team(1)
            self.create_unit(slim)
            test_list.append(slim)
        for i in range(15):
            slim = Slim(-1500 + i * 40, 300)
            slim.change_team(1)
            self.create_unit(slim)
            test_list.append(slim)
        test_building = Base(350, 0)
        self.create_unit(test_building)
        self.create_unit(Tree(0, 0))
        self.create_unit(Tree(-100, 0))
        self.create_unit(Tree(-200, 0))
        self.create_unit(Tree(-300, 0))
        self.create_unit(Tree(-400, 0))
        self.create_unit(Tree(-500, 0))

    def focus(self, unit):
        x = -unit.c_rect.left - unit.c_rect.width / 2 + 960
        self.set_camera([x, 0])

    def create_unit(self, unit):
        self.unit_list.append(unit)
        self.add(unit, projection=True, index=unit.layer)

    def unit_die(self, data):
        unit = data[0]
        trigger = data[1]
        if unit.exp_produce > 0 and trigger.team != unit.team and not TeamManager.is_alliance(trigger.team, unit.team):
            coll = pygame.Rect(unit.c_rect.left + unit.c_rect.width / 2 - 1300, 0, 2600, 1080)
            units = self.search_unit(coll)
            hero = list()
            for i in units:
                if i.flag.contain_flag("hero") and i.team == trigger.team:
                    hero.append(i)
            if trigger.flag.contain_flag("hero") and trigger not in hero:
                hero.append(trigger)
            for i in hero:
                i.attribute_manager.add_exp(unit.exp_produce / len(hero))
        self.unit_list.remove(unit)

    def search_unit(self, coll):
        unit_list = list()
        for i in self.unit_list:
            if i.get_volume_circle().collide(coll):
                unit_list.append(i)
        return unit_list

    def search_range(self, data):
        data[1].receive_unit_list(self.search_unit(data[0]))

    def create_trajectory(self, obj):
        self.add(obj, index=9)

    def create_special_effect(self, obj):
        self.add(obj, index=obj.index)

    def create_bullet(self, obj):
        self.add(obj, index=10)

    def skill_aim(self, skill):
        self.end_skill_aiming()
        self.aiming_skill = skill
        self.aiming_skill_target_mode = skill.target_mode
        if self.aiming_skill_target_mode is None:
            if self.aiming_skill.data_check(None):
                self.console.use_skill(self.aiming_skill, None)
                self.aiming_skill = None
        else:
            self.skill_aiming = True
            self.aiming_sight = self.aiming_skill.sight
            if self.aiming_sight is not None:
                self.aiming_sight.start_draw()
                if self.aiming_sight.show_mode == 0:
                    self.add(self.aiming_sight, index=-11)
                else:
                    self.add(self.aiming_sight, index=10)
            self.cursor.set_style("targetCHOOSE")
            self.cursor.lock()

    def end_skill_aiming(self):
        self.cursor.unlock()
        self.cursor.set_style("defeat")
        self.aiming_skill = None
        self.skill_aiming = False
        self.aiming_skill_target_mode = None
        if self.aiming_sight is not None:
            self.aiming_sight.end_draw()
            self.remove(self.aiming_sight)
            self.aiming_sight = None

    def cloud_cycle(self):
        for i in range(len(self.cloud_list)):
            if self.cloud_list[i].if_clear:
                left = i * 800 + random() * 800 - 800 - self.length / 2
                top = 100 + random() * 250
                speed = 9 + random() * 7
                last_time = 50 + random() * 30
                cloud = Background("cloud", "grassland", 0, pygame.Rect(left, top, 400, 200), speed, last_time,
                                   shadow_size=150,
                                   shadow_c=30)
                self.add(cloud, z=1, index=-101)
                self.cloud_list.pop(i)
                self.cloud_list.insert(i, cloud)

    def add_background(self, length):
        for i in range(length // 2600 + 1):
            self.add(Background("background", "grassland", 0,
                                pygame.Rect(-length / 2 - 1300 + i * 2600, 440, 2600, 500)), z=0.6, index=-103)

        for i in range(length // 2600 + 1):
            self.add(Background("background", "grassland", 3,
                                pygame.Rect(-length / 2 - 1000 + i * 2600, 350, 2600, 500)), z=0.45, index=-104)

        for i in range(length // 800 + 1):
            self.add(Background("fog", "grassland", 0, pygame.Rect(-length / 2 - 400 + i * 800, 420, 800, 200)),
                     z=0.35, index=-110)

        for i in range(length // 800 + 1):
            self.add(Background("fog", "grassland", 1, pygame.Rect(-length / 2 - 400 + i * 800, 550, 800, 200)),
                     z=0.35, index=-110)

    def message_add(self, data):
        self.add(data[0], data[1], data[2])

    def print_data(self, data):
        self.print_font.change_text(data)

    def set_frame(self, frame):
        self.frame.change_text("fps:" + str(frame))

    def map_shift(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x <= 10:
            self.move_camera([13, 0])
            self.projection_drawer.camera = self.camera_shifting[0]
            MessageManager.send_message("cursor_play", "arrowLEFT")
        elif mouse_x >= 1910:
            self.move_camera([-13, 0])
            self.projection_drawer.camera = self.camera_shifting[0]
            MessageManager.send_message("cursor_play", "arrowRIGHT")

    def add(self, display_object, index=0, z=1.0, projection=False):
        self.show_list.append([display_object, index, z, projection])
        self.show_list = sorted(self.show_list, key=(lambda x: [x[1]]))

    def radar_update(self, data):
        all_radar = []
        all_unit = []
        for i in self.unit_list:
            all_radar.append(i.get_radar())
            all_unit.append(i)

        for i in range(len(all_radar)):
            radar_list = []
            index_list = all_radar[i].collide_list(all_radar)
            index_list.remove(i)
            for i2 in index_list:
                radar_list.append(all_unit[i2])
            all_unit[i].radar_list = radar_list

    def surface_rendering(self, surface_list, object_list):
        if object_list[3] is True:
            return self.projection_drawer.draw(surface_list)
        else:
            return surface_list

    def update(self):
        self.map_shift()
        self.fog.set_c_shift(self.camera_shifting[0])
        self.fog.fog_update(self.unit_list)
        self.cloud_cycle()
        if self.aiming_prevent_up > 0:
            self.aiming_prevent_up -= 1

        self.mouse_double_click_record[1] -= 1 if self.mouse_double_click_record[1] > 0 else 0

        if pygame.mouse.get_pressed(3)[2] and self.if_pressed_right is False and self.skill_aiming is False and \
                pygame.mouse.get_pos()[1] < 835:
            self.if_pressed_right = True
            mouse = pygame.mouse.get_pos()
            mouse = [mouse[0], mouse[1]]
            mouse[0] -= self.camera_shifting[0]
            mouse[1] -= self.camera_shifting[1]
            if self.mouse_on is None or (self.mouse_on.flag.contain_flag("unit") or self.mouse_on.flag.contain_flag("resource")) is False:
                self.console.mouse_right_target(mouse)
            else:
                self.console.mouse_right_target(self.mouse_on)
        elif pygame.mouse.get_pressed(3)[2] and self.if_pressed_right is False and self.skill_aiming:
            self.if_pressed_right = True
            self.end_skill_aiming()
        elif pygame.mouse.get_pressed(3)[2] is False:
            self.if_pressed_right = False

        if self.mouse_on is not None and (self.mouse_on.flag.contain_flag("unit") or self.mouse_on.flag.contain_flag("resource")):
            cursor = "chooseDefeat"
            if TeamManager.is_player(self.mouse_on.team):
                cursor = "chooseOWN"
            elif TeamManager.is_alliance(TeamManager.player_team, self.mouse_on.team) is False:
                cursor = "chooseENEMY"
            MessageManager.send_message("cursor_play", cursor)

        if self.skill_aiming and len(self.mouse_drag_units) > 0:
            for i in self.mouse_drag_units:
                i.behavior_manager.remove_from_flag("preselection")
            self.mouse_drag_units = list()

        if self.aiming_skill is not None and self.aiming_skill.unit is None:
            self.end_skill_aiming()

        if self.skill_aiming:
            self.mouse_drag = False
            if self.mouse_on is None:
                self.cursor.unlock()
                self.cursor.set_style("targetCHOOSE")
                self.cursor.lock()
            elif TeamManager.is_player(self.mouse_on.team) and self.aiming_skill_target_mode.filter(self.mouse_on):
                self.cursor.unlock()
                self.cursor.set_style("targetOWN")
                self.cursor.lock()
            elif TeamManager.is_alliance(TeamManager.player_team, self.mouse_on.team) is False and \
                    self.aiming_skill_target_mode.filter(self.mouse_on):
                self.cursor.unlock()
                self.cursor.set_style("targetENEMY")
                self.cursor.lock()
            elif TeamManager.is_alliance(TeamManager.player_team, self.mouse_on.team)and \
                    self.aiming_skill_target_mode.filter(self.mouse_on):
                self.cursor.unlock()
                self.cursor.set_style("targetAlly")
                self.cursor.lock()
            else:
                self.cursor.unlock()
                self.cursor.set_style("targetCHOOSE")
                self.cursor.lock()
            if self.aiming_sight is not None:
                if_mouse_on = self.mouse_on is not None
                target_accept = self.aiming_skill_target_mode.filter(self.mouse_on) if if_mouse_on else False
                if if_mouse_on is False or target_accept is False:
                    pos = list(pygame.mouse.get_pos())
                    pos[0] -= self.camera_shifting[0]
                    pos[1] -= self.camera_shifting[1]
                    self.aiming_sight.draw(pos)
                elif target_accept:
                    self.aiming_sight.draw(self.mouse_on)

        if self.mouse_drag:
            mouse = pygame.mouse.get_pos()
            x_different = self.mouse_down_c[0] - mouse[0]
            y_different = self.mouse_down_c[1] - mouse[1]
            distance = math.sqrt(x_different ** 2 + y_different ** 2)
            if distance > 25 and abs(x_different) > 4 and abs(y_different) > 4:
                left = self.mouse_down_c[0] if x_different < 0 else mouse[0]
                top = self.mouse_down_c[1] if y_different < 0 else mouse[1]
                rect = pygame.Rect(left, top, abs(x_different), abs(y_different))
                pygame.draw.rect(self.father_surface, color=(160, 255, 160), rect=rect, width=2)

                rect.left -= self.camera_shifting[0]
                rect.height -= self.camera_shifting[1]

                for i in self.show_list:
                    i = i[0]
                    if i.flag.contain_flag(["unit"]) and TeamManager.is_player(i.team) and i.visible \
                            and i.in_screen and i not in self.mouse_drag_units:
                        circle = Circle(0, 0, 0)
                        circle.load_from_rect(i.c_rect, i.volume)
                        if circle.collide(rect):
                            self.mouse_drag_units.append(i)
                            i.behavior_manager.add(Preselection())
                for i in self.mouse_drag_units:
                    circle = Circle(0, 0, 0)
                    circle.load_from_rect(i.c_rect, i.volume)
                    if circle.collide(rect) is False:
                        self.mouse_drag_units.remove(i)
                        i.behavior_manager.remove_from_flag("preselection")
            else:
                for i in self.mouse_drag_units:
                    i.behavior_manager.remove_from_flag("preselection")
                self.mouse_drag_units = list()

    def mouse_down_pos(self, mouse):
        if mouse[1] < 830 and self.skill_aiming is False:
            self.mouse_down_c = mouse
            self.mouse_drag = True
        if self.skill_aiming:
            filter_object = list(mouse)
            filter_object[0] -= self.camera_shifting[0]
            filter_object[1] -= self.camera_shifting[1]
            filter_point = filter_object
            if self.mouse_on is not None and (self.mouse_on.flag.contain_flag("unit") or self.mouse_on.flag.contain_flag("resource")):
                filter_object = self.mouse_on
            if self.aiming_skill_target_mode.filter(filter_object) and self.aiming_skill.data_check(filter_object):
                self.console.use_skill(self.aiming_skill, filter_object)
                if KeyListener.get_key(pygame.K_LSHIFT) is False:
                    self.end_skill_aiming()
                    self.aiming_prevent_up = 8
            elif self.aiming_skill_target_mode.filter(filter_point) and self.aiming_skill.data_check(filter_point):
                self.console.use_skill(self.aiming_skill, filter_point)
                if KeyListener.get_key(pygame.K_LSHIFT) is False:
                    self.end_skill_aiming()
                    self.aiming_prevent_up = 8

    def mouse_up_pos(self, mouse):
        self.mouse_drag = False
        if len(self.mouse_drag_units) > 0:
            self.console.set_units(self.mouse_drag_units)
        for i in self.mouse_drag_units:
            i.behavior_manager.remove_from_flag("preselection")
        self.mouse_drag_units = list()

    def mouse_enter(self, target, mouse):
        if (target.flag.contain_flag("unit") or target.flag.contain_flag("resource")) and self.mouse_drag is False:
            target.behavior_manager.add(Preselection())

    def mouse_leave(self, target, mouse):
        if (target.flag.contain_flag("unit") or target.flag.contain_flag("resource")) and target not in self.mouse_drag_units:
            target.behavior_manager.remove_from_flag("preselection")

    def mouse_click(self, target, mouse):
        if (target.flag.contain_flag("unit") or target.flag.contain_flag("resource"))\
                and self.skill_aiming is False and self.aiming_prevent_up <= 0:
            if self.mouse_double_click_record[0] == target and self.mouse_double_click_record[1] > 0 and \
                    TeamManager.is_player(target.team):
                left = target.c_rect.left + target.c_rect.width / 2 - 750
                search_rect = pygame.Rect(left, 0, 1500, 1080)
                unit_list = self.search_unit(search_rect)
                units = list()
                for i in unit_list:
                    if TeamManager.is_player(i.team) and i.flag.flag == target.flag.flag:
                        units.append(i)
                self.console.set_units(units)
            else:
                self.console.set_units([target])
                self.mouse_double_click_record[0] = target
                self.mouse_double_click_record[1] = 15
