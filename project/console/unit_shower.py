from base import Base
from console.close_up import CloseUp
from console.skill_shower import SkillShower
from console.armor_shower import ArmorShower
from console.weapon_shower import WeaponShower
from console.units_button import UnitButton
from console.exp_button import ExpButton
from console.formation_button import FormationButton
from console.behavior_button import BehaviorButton
from console.production_button import ProductionButton
from console.console_text import ConsoleText
from display.atlas import Atlas
from display.font import FontSurface
from auxiliary_tools.key_listener import KeyListener
from auxiliary_tools.message_manager import MessageManager
from unit_tools.team_manager import TeamManager
from units.behaviors.chosen import Chosen
from copy import copy
import pygame


class UnitShower(Base):
    def __init__(self):
        super().__init__()
        self.unit_list = []
        self.frame_background = Atlas.load("./data/img/console", "UnitShower")["defeat"][0][0]
        self.surface = pygame.Surface((630, 250))
        self.surface.set_colorkey((0, 0, 0))
        self.c_rect = pygame.Rect(480, 830, 630, 250)
        self.surface.blit(self.frame_background, [0, 0])
        self.close_up = CloseUp()
        self.skill_shower = SkillShower()

        self.weapons_button_list = list()
        self.units_button_list = list()
        self.behaviors_button_list = list()
        self.formation_button_list = list()
        self.behavior_list = list()
        self.panel_dict = None
        self.physical_armor_shower = ArmorShower([-100, -100], armor_type=0)
        self.magic_armor_shower = ArmorShower([-100, -100], armor_type=1)
        self.exp_button = ExpButton([-100, -100])
        self.production_button = ProductionButton(-300, -300)
        self.text = ConsoleText()

        self.name = pygame.Surface((0, 0))
        self.label = pygame.Surface((0, 0))

        self.units_index = 0

        self.message_require("choose_units", self.mes_set_units)
        self.message_require("key_down", self.key_down)
        self.message_require("FormationChoose", self.formation_change)

    def use_skill(self, skill, data):
        self.skill_shower.use_skill(skill, data)

    def use_skill_by_flag(self, skill_flag, data):
        self.skill_shower.use_skill_by_flag(skill_flag, data)

    def key_down(self, data):
        if data[0] == pygame.K_TAB:
            unit_flag = self.unit_list[self.units_index].flag.flag
            find = False
            page_before = self.units_index // 24 + 1
            for i in range(self.units_index, len(self.unit_list)):
                if self.unit_list[i].flag.contain_flag(unit_flag, must_have_all=True) is False:
                    find = True
                    self.units_index = i
                    break
            if find is False:
                self.units_index = 0
            for i in self.units_button_list:
                i.set_high_light(self.unit_list[self.units_index].flag.flag)
            page_now = self.units_index // 24 + 1
            self.skill_shower.set_now_units(self.unit_list[self.units_index].flag.flag)
            self.close_up.set_unit(self.unit_list[self.units_index])
            if page_before != page_now:
                MessageManager.send_message("FormationChoose", page_now)

    def formation_change(self, page):
        for i in self.units_button_list:
            i.clear()
        self.units_button_list = list()
        page = int(page)
        page -= 1
        for i in range(page * 24, len(self.unit_list)):
            if i > page * 24 + 23:
                break
            x = 560 + (i - page * 24) % 8 * 60
            y = 900 + (i - page * 24) // 8 * 60
            self.units_button_list.append(UnitButton([x, y], self.unit_list[i]))
        for i in self.units_button_list:
            i.set_high_light(self.unit_list[self.units_index].flag.flag)

    def mouse_right_target(self, data):
        self.skill_shower.mouse_right_target(data)

    def mes_set_units(self, data):
        self.choose_units(data)

    def choose_units(self, units):
        if KeyListener.get_key(pygame.K_LSHIFT) is False or TeamManager.is_player(units[0].team) is False:
            self.set_units(units)
        else:
            unit_list = list()
            for i in self.unit_list:
                unit_list.append(i)
            if len(units) > 1:
                for i in units:
                    if i not in self.unit_list:
                        unit_list.append(i)
                self.set_units(unit_list)
            elif len(units) == 1:
                unit = units[0]
                if unit not in self.unit_list:
                    unit_list.append(unit)
                else:
                    unit_list.remove(unit)
                self.set_units(unit_list)

    def set_units(self, units):
        for i in self.weapons_button_list:
            i.clear()
        self.weapons_button_list = list()
        for i in self.units_button_list:
            i.clear()
        self.units_button_list = list()
        for i in self.formation_button_list:
            i.clear()
        self.formation_button_list = list()
        for i in self.behaviors_button_list:
            i.clear()
        self.behaviors_button_list = list()
        for i in self.unit_list:
            i.behavior_manager.remove_from_flag("chosen")
        self.behavior_list = list()

        if units is not None:
            units = sorted(units, key=(lambda index: [index.order, index.unit_panel["name"]]), reverse=True)
            self.close_up.set_unit(units[0])
            self.skill_shower.set_unit(units)
            self.units_index = 0
            for i in units:
                i.behavior_manager.add(Chosen())
            if len(units) == 1:
                unit = units[0]
                self.panel_dict = copy(unit.unit_panel)
                self.name = FontSurface(unit.unit_panel["name"], 25, color=(230, 230, 200)).surface
                label = "-"
                for i in unit.unit_panel["unit_label"]:
                    label += i + "-"
                self.label = FontSurface(label, 15, color=(200, 200, 200)).surface

                if unit.unit_panel.get("base_info") is not None:
                    base_y = unit.unit_panel["base_info"]

                    self.physical_armor_shower.set_unit(unit)
                    self.magic_armor_shower.set_unit(unit)

                    button_amount = len(unit.weapons.weapons) + 2
                    for i in range(len(unit.weapons.weapons)):
                        x = 780 - 70 * button_amount / 2 + i * 70
                        self.weapons_button_list.append(WeaponShower(unit.weapons.weapons[i], (x, 925 + base_y)))
                    x = 780 + 70 * button_amount / 2 - 140
                    self.physical_armor_shower.move_to(x, 925 + base_y)
                    self.magic_armor_shower.move_to(x + 70, 925 + base_y)
                else:
                    self.physical_armor_shower.set_unit(None)
                    self.magic_armor_shower.set_unit(None)
                    self.physical_armor_shower.move_to(-100, -100)
                    self.magic_armor_shower.move_to(-100, -100)

                if unit.unit_panel.get("exp_info") is not None:
                    base_y = unit.unit_panel["exp_info"]

                    self.exp_button.set_unit(unit)
                    self.exp_button.move_to(575, base_y + 925)
                else:
                    self.exp_button.set_unit(None)
                    self.exp_button.move_to(-100, -100)

                if unit.unit_panel.get("production_info") is not None:
                    self.production_button.set_unit(unit)
                    self.production_button.move_to(600, unit.unit_panel["production_info"] + 925)
                else:
                    self.production_button.set_unit(None)
                    self.production_button.move_to(-300, -300)

                if unit.unit_panel.get("text") is not None:
                    self.text.set_unit(unit)
                else:
                    self.text.set_unit(None)

                for i in unit.behavior_manager.behavior_list:
                    if i.icon_visible:
                        self.behavior_list.append(i)
                for i in range(len(self.behavior_list)):
                    x = 500
                    y = 900 + i * 35
                    behavior_button = BehaviorButton((x, y), self.behavior_list[i])
                    self.behaviors_button_list.append(behavior_button)

            else:
                self.text.set_unit(None)
                self.exp_button.set_unit(None)
                self.production_button.set_unit(None)
                self.physical_armor_shower.set_unit(None)
                self.magic_armor_shower.set_unit(None)
                self.panel_dict = None
                page_amount = len(units) // 24 + 1
                for i in range(1, page_amount + 1):
                    x = 500
                    y = 870 + i * 30
                    button = FormationButton([x, y], corner=i)
                    self.formation_button_list.append(button)
                for i in range(len(units)):
                    if i > 23:
                        break
                    x = 560 + i % 8 * 60
                    y = 900 + i // 8 * 60
                    self.units_button_list.append(UnitButton([x, y], units[i]))
                for i in self.units_button_list:
                    i.set_high_light(units[0].flag.flag)

            self.unit_list = units
            self.update()
        else:
            self.unit_list = []
            self.close_up.set_unit(None)
            self.skill_shower.set_unit(None)

    def set_list(self, unit_list):
        self.unit_list = unit_list

    def get_surface(self):
        surface_list = list()
        surface_list.append([self.surface, self.c_rect])
        for i in self.close_up.get_surface():
            surface_list.append(i)
        for i in self.skill_shower.get_surface():
            surface_list.append(i)
        if self.unit_list is not None:
            if len(self.unit_list) == 1:
                surface_list.append([self.name, pygame.Rect(780 - self.name.get_width() / 2, 865, 100, 100)])
                surface_list.append([self.label, pygame.Rect(780 - self.label.get_width() / 2, 900, 250, 100)])
                surface_list.append(self.text.get_surface())
                for i in self.exp_button.get_surface():
                    surface_list.append(i)
                for i in self.production_button.get_surface():
                    surface_list.append(i)
                for i in self.physical_armor_shower.get_surface():
                    surface_list.append(i)
                for i in self.magic_armor_shower.get_surface():
                    surface_list.append(i)
                for i in self.weapons_button_list:
                    for i2 in i.get_surface():
                        surface_list.append(i2)
                for i in self.behaviors_button_list:
                    for i2 in i.get_surface():
                        surface_list.append(i2)
            else:
                for i in self.units_button_list:
                    for i2 in i.get_surface():
                        surface_list.append(i2)
                for i in self.formation_button_list:
                    for i2 in i.get_surface():
                        surface_list.append(i2)
        return surface_list

    def get_close_up_unit(self):
        return self.unit_list[0]

    def update(self):
        if self.unit_list is not None:
            self.close_up.update()
            self.skill_shower.update()
            if len(self.unit_list) == 1:
                if self.unit_list[0].unit_panel != self.panel_dict:
                    self.set_units(self.unit_list)
                    return
                self.text.update()
                self.exp_button.update()
                self.production_button.update()
                self.physical_armor_shower.update()
                self.magic_armor_shower.update()
                for i in self.weapons_button_list:
                    i.update()
                behavior_list_now = list()
                for i in self.unit_list[0].behavior_manager.behavior_list:
                    if i.icon_visible:
                        behavior_list_now.append(i)
                if behavior_list_now != self.behavior_list:
                    self.behavior_list = behavior_list_now
                    for i in self.behaviors_button_list:
                        i.clear()
                    self.behaviors_button_list = list()
                    for i in range(len(self.behavior_list)):
                        x = 500
                        y = 900 + i * 35
                        behavior_button = BehaviorButton((x, y), self.behavior_list[i])
                        self.behaviors_button_list.append(behavior_button)
                for i in self.behaviors_button_list:
                    i.update()
            else:
                for i in self.units_button_list:
                    i.update()
                for i in self.formation_button_list:
                    i.update()

        wait_to_clean = []
        for i in self.unit_list:
            if i.wait_to_death is True:
                wait_to_clean.append(i)
        for i in wait_to_clean:
            self.unit_list.remove(i)
        if len(self.unit_list) == 0:
            self.set_units(None)
        elif len(self.unit_list) == 1 and len(wait_to_clean) != 0:
            self.set_units(self.unit_list)

        if self.units_index > len(self.unit_list) - 1:
            self.units_index = len(self.unit_list) - 1
        if len(wait_to_clean) > 0:
            for i in self.units_button_list:
                i.set_high_light(self.unit_list[self.units_index].flag.flag)

        if self.close_up.unit is None and len(self.unit_list) != 0:
            self.close_up.set_unit(self.get_close_up_unit())

    def clear(self):
        super().clear()
        self.close_up.clear()
        self.skill_shower.clear()
        self.physical_armor_shower.clear()
        self.magic_armor_shower.clear()
        self.exp_button.clear()
        self.production_button.clear()

        self.close_up = None
        self.skill_shower = None
        self.physical_armor_shower = None
        self.magic_armor_shower = None
        self.exp_button = None
        self.production_button = None

        for i in self.behaviors_button_list:
            i.clear()
        for i in self.units_button_list:
            i.clear()
        for i in self.formation_button_list:
            i.clear()
        for i in self.weapons_button_list:
            i.clear()
        self.behaviors_button_list = list()
        self.units_button_list = list()
        self.formation_button_list = list()
        self.weapons_button_list = list()

        self.unit_list = list()
        self.units_index = 0
