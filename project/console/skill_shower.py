from base import Base
from console.skill_button import SkillButton
from console.panel_button import PanelButton
from display.atlas import Atlas
from auxiliary_tools.message_manager import MessageManager
from auxiliary_tools.key_listener import KeyListener
from units.indicators.move_indicator import MoveIndicator
from unit_tools.team_manager import TeamManager
import pygame


class SkillShower(Base):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((360, 265))
        self.surface.set_colorkey((0, 0, 0))
        self.c_rect = pygame.Rect(1130, 815, 360, 265)
        self.background001 = Atlas.load("./data/img/console", "SkillShower")["defeat"][0][0]
        self.background002 = Atlas.load("./data/img/console", "SkillShower")["defeat"][1][0]
        self.surface = self.background001

        self.now_units = list()
        self.all_units = list()
        self.button_list = list()
        self.mouse_skill = list()
        self.panel = "defeat"
        self.skill_replace_index = 0

        self.enabled = False

        self.message_require("change_auto_use", self.change_auto_use)
        self.message_require("panel_to", self.change_panel)

    def change_panel(self, target_panel):
        self.panel = target_panel
        self.reset_button_list()

    def change_auto_use(self, data):
        if self.enabled:
            for i in self.all_units:
                skill = i.skill_manager.get(data[0])
                if skill is not None:
                    skill.if_auto_use = data[1]

    def mouse_right_target(self, data):
        if self.enabled:
            clear = "None" if KeyListener.get_key(pygame.K_LSHIFT) else "clear"
            left_volume = 0
            for i in self.all_units:
                left_volume += i.volume
            left_volume += (len(self.all_units) - 1) * 2
            for i in self.all_units:
                if i.state_label.contain_flag("uncontrollable") is False:
                    skill = i.skill_manager.filter_target(data, skill_limit=self.mouse_skill)
                    if skill is not None and skill.if_ready:
                        if skill.flag.contain_flag("move") and type(data) is list:
                            MessageManager.send_message("add_indicator", MoveIndicator(data[0]))
                            move_data = [data[0], 0]
                            move_data[0] -= left_volume - i.volume
                            left_volume -= i.volume * 2 + 4
                            i.controller.use_skill(skill.flag.flag, move_data, clear)
                        else:
                            i.controller.use_skill(skill.flag.flag, data, clear)

    def use_skill(self, skill, data):
        if self.enabled:
            clear = "None" if KeyListener.get_key(pygame.K_LSHIFT) else "clear"
            replace = skill.quick_spell is False and skill.flag.contain_flag("instruction_replace")
            if replace:
                # 优先使用指令数最小的技能
                smallest_count = 100
                smallest_unit = None
                for i in self.all_units:
                    if i.state_label.contain_flag("uncontrollable") is False:
                        skill_get = i.skill_manager.get(skill.flag.flag)
                        if skill_get is not None and skill_get.if_ready and skill_get.instruction_count < smallest_count:
                            smallest_unit = i
                            smallest_count = skill_get.instruction_count

                if smallest_unit is not None:
                    smallest_unit.controller.use_skill(skill.flag.flag, data, clear)
                    return

                # 若都已获取过指令， 则逐个替换原有的指令
                i = self.skill_replace_index
                circle = False
                while True:
                    skill_get = self.all_units[i].skill_manager.get(skill.flag.flag)
                    if skill_get is not None and skill_get.if_ready:
                        self.all_units[i].controller.replace_skill_instruction(skill.flag.flag, data)
                        break
                    i += 1
                    if i > len(self.all_units) - 1:
                        i = 0
                    if i == self.skill_replace_index and circle:
                        break
                    circle = True
                self.skill_replace_index = i + 1
                if self.skill_replace_index > len(self.all_units) - 1:
                    self.skill_replace_index = 0
            else:
                # 若不进行替换，则正常进行技能使用
                for i in self.all_units:
                    if i.state_label.contain_flag("uncontrollable") is False:
                        skill_get = i.skill_manager.get(skill.flag.flag)
                        if skill_get is not None and skill_get.if_ready:
                            i.controller.use_skill(skill.flag.flag, data, clear)
                            if skill.quick_spell is False:
                                break

    def use_skill_by_flag(self, skill_flag, data):
        if self.enabled:
            clear = "None" if KeyListener.get_key(pygame.K_LSHIFT) else "clear"
            for i in self.all_units:
                if i.state_label.contain_flag("uncontrollable") is False:
                    skill_get = i.skill_manager.get(skill_flag)
                    if skill_get is not None and skill_get.if_ready and skill_get.ready_to_use is False:
                        i.controller.use_skill(skill_flag, data, clear)
                        if skill_get.quick_spell is False:
                            return

    def reset_button_list(self):
        for i in self.button_list:
            i.clear()
        self.button_list = []
        index = 0
        for i in range(len(self.now_units)):
            if self.now_units[i].wait_to_death is False:
                index = i
                break
        if len(self.now_units) <= 0:
            return
        if self.now_units[index].state_label.contain_flag("uncontrollable") or \
                not TeamManager.is_player(self.now_units[index].team):
            return
        self.now_units[index].skill_panel.panel_change = False
        for i in range(len(self.now_units[index].skill_panel.get_panel(self.panel))):
            if self.now_units[index].skill_panel.get_panel(self.panel)[i][0] is not None:
                panel = self.now_units[index].skill_panel.panel[self.panel][i]
                x = i % 5 * 60 + 1160
                y = i // 5 * 60 + 835
                icon = panel[0]
                skill = panel[1]
                key = panel[2]
                mouse = panel[3]
                describe = panel[4]
                panel_to = panel[5]
                if mouse:
                    self.mouse_skill.append(skill.flag.flag)
                if panel_to is None:
                    button = SkillButton([x, y], img=icon, skill=skill, key=key, mouse=mouse, describe=describe)
                else:
                    button = PanelButton([x, y], icon=icon, panel_to=panel_to, describe=describe, key=key)
                self.button_list.append(button)

    def set_now_units(self, unit_flag):
        for i in self.button_list:
            i.clear()
        self.button_list = []
        self.now_units = []
        for i in self.all_units:
            if i.flag.contain_flag(unit_flag, must_have_all=True):
                self.now_units.append(i)
        self.reset_button_list()

    def set_unit(self, units):
        for i in self.button_list:
            i.clear()
        self.button_list = []
        self.now_units = []
        self.all_units = []
        self.mouse_skill = []
        self.skill_replace_index = 0
        if units is None or (TeamManager.is_player(units[0].team) and
                             units[0].state_label.contain_flag("uncontrollable") is False):
            self.surface = self.background001
            self.enabled = True
            if units is not None:
                self.panel = "defeat"
                self.all_units = units
                flag = units[0].flag.flag
                units_list = []
                for i in units:
                    if i.flag.contain_flag(flag, must_have_all=True):
                        units_list.append(i)
                self.now_units = units_list

                self.reset_button_list()
            else:
                self.now_units = list()
                self.panel = "defeat"
        else:
            self.all_units = units
            self.now_units = units
            self.surface = self.background002
            self.enabled = False

    def update(self):
        remove_list = list()
        for i in self.now_units:
            if i.wait_to_death:
                remove_list.append(i)
        for i in remove_list:
            self.now_units.remove(i)
        if len(remove_list) > 0:
            self.reset_button_list()

        remove_list = list()
        for i in self.all_units:
            if i.wait_to_death:
                remove_list.append(i)
        for i in remove_list:
            self.all_units.remove(i)

        if len(self.all_units) == 0:
            self.set_unit(None)
        elif len(self.now_units) != 0 and self.now_units[0].skill_panel.panel_change:
            self.reset_button_list()

        for i in self.button_list:
            if type(i) is SkillButton:
                skill_now = i.skill
                if skill_now.if_ready is False:
                    final_skill = None
                    now_cooling = skill_now.cooling_time
                    for i2 in self.all_units:
                        skill_else = i2.skill_manager.get(skill_now.flag.flag)
                        if skill_else is not None and skill_else.if_ready:
                            final_skill = skill_else
                            break
                        elif skill_else is not None and skill_else.enabled and skill_else.resource_ample():
                            else_cooling = skill_else.cooling_time
                            if else_cooling < now_cooling:
                                final_skill = skill_else
                                now_cooling = else_cooling
                    if final_skill is not None:
                        i.set_skill(final_skill)

        for i in self.button_list:
            i.update()

    def get_surface(self):
        surface_list = list()
        surface_list.append([self.surface, self.c_rect])
        for i in self.button_list:
            for i2 in i.get_surface():
                surface_list.append(i2)
        return surface_list

    def clear(self):
        super().clear()

        for i in self.button_list:
            i.clear()

        self.now_units = list()
        self.all_units = list()
        self.button_list = list()
        self.mouse_skill = list()
