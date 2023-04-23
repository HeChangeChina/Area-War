from display.normal_display import NormalDisplay
from auxiliary_tools.flag_manager import FlagManager
from auxiliary_tools.circle import Circle
from auxiliary_tools.message_manager import MessageManager
from auxiliary_tools.resources_manager import ResourcesManager
from auxiliary_tools.exact_rect import ERect
from unit_tools.height_controller import HeightController
from unit_tools.unit_instructor import UnitInstructor
from unit_tools.skill_manager import SkillManager
from unit_tools.unit_controller import UnitController
from unit_tools.weapon_manager import WeaponManager
from console.skill_panel import SkillPanel
import pygame


class Unit(NormalDisplay):
    def __init__(self, atlas, unit_name, c_rect, attribute_manager, unit_height=280, unit_height_c=0,
                 weapons=None, team=0, volume=15, radar_range=400, population_cost=0, population_produce=0):
        super().__init__(atlas, unit_name, c_rect, base_event=False)
        self.flag.add_flag("unit") 
        self.message_require("update_60", self.unit_base_update_60)
        self.message_require("update_15", self.unit_base_update_15)
        self.attribute_manager = attribute_manager
        self.behavior_manager = self.attribute_manager.behavior_manager
        self.behavior_manager.set_unit(self)
        self.height_controller = HeightController(1080 - self.c_rect.top + unit_height_c, 280 + unit_height_c)
        self.wait_to_death = False
        self.unit_height = unit_height
        self.unit_height_c = unit_height_c
        self.weapons = weapons
        self.show_list = []
        rect = self.c_rect
        self.c_rect = ERect()
        self.c_rect.load_rect(rect)
        self.mouse_enabled = True

        if self.weapons is None:
            self.weapons = WeaponManager()

        self.instructor = UnitInstructor(self)
        self.skill_manager = SkillManager()
        self.skill_panel = SkillPanel()
        self.controller = UnitController(self.skill_manager, self.instructor, self)

        self.radar_range = radar_range
        self.radar_list = []
        self.radar = Circle(self.c_rect.left + self.c_rect.width / 2 - self.radar_range,
                            self.c_rect.top + self.c_rect.height / 2 - self.radar_range,
                            self.radar_range)
        self.volume = volume
        self.team = team
        self.exp_produce = 10
        self.state_label = FlagManager()
        self.cost = dict()
        self.population_cost = population_cost
        self.population_produce = population_produce

        self.visual_field = 600

        ResourcesManager.add_resources("max_population", self.population_produce, self.team)
        ResourcesManager.add_resources("population", self.population_cost, self.team)

        self.event_prevent = False

        # 以下是一些只会对视觉效果产生影响的属性，并非必需
        self.unit_panel = dict()
        self.unit_panel["base_info"] = 20
        self.unit_panel["close_up_background"] = "defeat"
        self.unit_panel["armor_icon"] = ("armor", "armor")
        self.unit_panel["armor_name"] = ("物理护甲", "法术抗性")
        self.unit_panel["name"] = "单位"
        self.unit_panel["title"] = "一个伟大的单位"
        self.unit_panel["unit_icon"] = "UnitIcon"
        self.unit_panel["unit_label"] = list()
        self.unit_panel["text"] = None
        self.unit_panel["text_y"] = 35
        self.aiming_animation = None
        self.base_bullet_anchor = [15, 0]
        self.bullet_anchor = [15, 0]
        self.order = 0
        self.layer = 1

    def change_team(self, team):
        ResourcesManager.add_resources("max_population", -self.population_produce, self.team)
        ResourcesManager.add_resources("population", -self.population_cost, self.team)

        ResourcesManager.add_resources("max_population", self.population_produce, team)
        ResourcesManager.add_resources("population", self.population_cost, team)

        self.attribute_manager.change_team(team)

        for i in self.weapons.weapons:
            i.change_team(team)

        self.team = team

    def get_volume_circle(self):
        left = self.c_rect.left + self.c_rect.width / 2 - self.volume
        top = self.c_rect.top + self.c_rect.height / 2 - self.volume
        volume_circle = Circle(left, top, self.volume)
        return volume_circle

    def get_radar(self):
        self.radar.left = self.c_rect.left + self.c_rect.width / 2 - self.radar_range
        self.radar.top = self.c_rect.top + self.c_rect.height / 2 - self.radar_range
        self.radar.radius = self.radar_range
        return self.radar

    def add_surface(self, surface, shifting, flag):
        self.show_list.append([surface, shifting, flag])

    def remove_surface(self, flag):
        for i in self.show_list:
            if i[2] == flag:
                self.show_list.remove(i)
                break

    def replace_surface(self, surface, shifting, flag):
        for i in range(len(self.show_list)):
            if self.show_list[i][2] == flag:
                self.show_list[i][0] = surface
                self.show_list[i][1] = shifting
                break

    def get_surface(self):
        show_list = [[self.shader.get_surface(), self.c_rect.rect()]]
        for i in self.show_list:
            rect = pygame.Rect(self.c_rect.left + i[1].left, self.c_rect.top + i[1].top, self.c_rect.width + i[1].width,
                               self.c_rect.height + i[1].height)
            show_list.append([i[0], rect])
        return show_list

    def unit_base_update_60(self, data):
        self.weapons.weapon_speed = self.attribute_manager.get_attribute("weapon_speed")

        self.animate_controler.animate_update(None)
        self.attribute_manager.update()
        self.behavior_manager.update_60()
        self.height_controller.update()
        self.skill_manager.update()
        self.instructor.update()
        self.controller.base_update()
        self.c_rect.top = 1080 - self.height_controller.height
        self.weapons.update()
        if self.animate_controler.now_side == 0:
            self.bullet_anchor[0] = self.base_bullet_anchor[0]
            self.bullet_anchor[1] = self.base_bullet_anchor[1]
        else:
            self.bullet_anchor[0] = -self.bullet_anchor[0]
            self.bullet_anchor[1] = self.base_bullet_anchor[1]
        self.update_60()

    def update_60(self):
        pass

    def unit_base_update_15(self, data):
        self.behavior_manager.update_15()
        self.update_15()

    def update_15(self):
        pass

    def clear(self):
        super().clear()
        self.visible = False
        self.if_clear = True
        self.radar_list = []
        self.attribute_manager.clear()
        self.behavior_manager.clear()
        self.height_controller.clear()
        self.instructor.clear()
        self.weapons.clear()
        self.skill_panel.clear()
        self.skill_manager.clear()

    def death(self, trigger):
        MessageManager.send_message("unit_die", (self, trigger))
        if self.event_prevent is False:
            self.wait_to_death = True
            self.behavior_manager.clear_behaviors()
            self.instructor.compulsorily_clear_instructions()
            self.instructor.enabled = False
            self.animate_controler.stop = False
            self.animate_controler.play_action("death", end_recall=self.clear, lock=True)

            ResourcesManager.add_resources("max_population", -self.population_produce, self.team)
            ResourcesManager.add_resources("population", -self.population_cost, self.team)
        else:
            self.event_prevent = False
