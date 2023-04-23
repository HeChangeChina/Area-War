from console.console_button import ConsoleButton
from display.atlas import Atlas
from display.font import FontSurface
from auxiliary_tools.message_manager import MessageManager
from auxiliary_tools.key import Key
import pygame
import math


class SkillButton(ConsoleButton):
    def __init__(self, c_xy, skill, img="skill", key=None, mouse=None, describe="技能"):
        self.skill = skill
        self.key = str(key) if key is not None else None
        self.mouse = mouse
        self.describe = describe
        self.base_describe = self.describe
        self.img = img

        self.resource_surface = None
        self.resource_rect = None
        self.high_light_time = 0
        self.mouse_right_down = False
        self.auto_use_time = 0

        self.base_pressed_prevent = 3

        self.resource_require = []
        text_shift = 0
        if self.skill.magic_require > 0:
            self.resource_require.append(["magic", self.skill.magic_require])
        for i in self.skill.resource_cost_show:
            self.resource_require.append([i, self.skill.resource_cost_show[i]])
        if len(self.resource_require) > 0:
            text_shift = -40

        self.auto_use = self.skill.can_auto_use
        self.skill_surface = Atlas.load("./data/img/skill_icon", self.img)["defeat"][0][0]
        self.skill_ban_surface = pygame.Surface((60, 60))
        self.skill_ban_surface.blit(self.skill_surface, (0, 0))
        self.skill_ban_surface.blit(Atlas.load("./data/img/console", "SkillBan")["defeat"][0][0], (0, 0))
        self.skill_surface_out_of_magic = pygame.Surface((60, 60))
        self.skill_surface_out_of_magic.blit(self.skill_surface, (0, 0))
        self.skill_surface_out_of_magic.fill((155, 155, 255), special_flags=pygame.BLEND_MULT)

        if self.auto_use is False:
            self.frame = "NormalSkillFrame"
        else:
            self.frame = "AutoSkillFrame"

        super().__init__(c_xy=c_xy, img=img, frame=self.frame, text=self.describe, corner=key,
                         corner_color=(230, 230, 170), text_shift=text_shift)

        if self.key is not None:
            self.key_code = Key.get_code_by_key(self.key)
            self.message_require("key_down", self.key_down)
        else:
            self.key_code = None

        if len(self.resource_require) > 0:
            self.resource_show()
        self.update()

    def key_down(self, key):
        if key[0] == self.key_code and self.base_pressed_prevent == 0:
            self.mouse_down()

    def mouse_down(self):
        if self.skill.if_ready:
            self.high_light_time = 5
            MessageManager.send_message("skill_aim", self.skill)

    def resource_show(self):
        self.resource_surface = pygame.Surface((85, len(self.resource_require) * 30 + 3))
        height = self.resource_surface.get_height()
        top = self.text_rect.top if self.text_rect.height > height else self.text_rect.top - height + self.text_rect.height
        self.resource_rect = pygame.Rect(self.text_rect.left + 165, top, 50, height)
        self.resource_surface.fill((100, 100, 150))
        pygame.draw.rect(self.resource_surface, (240, 210, 160), pygame.Rect(0, 0, 85, height), 3)
        for i in range(len(self.resource_require)):
            icon_surface = Atlas.load("./data/img/console", self.resource_require[i][0])["defeat"][0][0]
            self.resource_surface.blit(icon_surface, (6, 6 + 30 * i))
            font = FontSurface(str(self.resource_require[i][1]), 18).surface
            self.resource_surface.blit(font, (32, 6 + 30 * i))

    def set_skill(self, skill):
        self.skill = skill

    def update(self):
        super().update()
        if self.base_pressed_prevent > 0:
            self.base_pressed_prevent -= 1

        if self.skill is not None:
            surface = pygame.Surface((60, 60))
            if self.skill.magic_ample is False:
                surface.blit(self.skill_surface_out_of_magic, (0, 0))
            else:
                surface.blit(self.skill_surface, (0, 0))
            if self.skill.cooling_time > 0:
                cooling_surface = pygame.Surface((60, 60))
                cooling_surface.set_colorkey((0, 0, 0))
                cooling_time = self.skill.cooling_time
                cooling = self.skill.cooling * 60
                cooling_rate = 1 - cooling_time / cooling
                angle = cooling_rate * math.pi * 2 - math.pi
                points_list = list()
                points_list.append((30, 30))
                cooling_point = [30 - math.sin(angle) * 45, 30 + math.cos(angle) * 45]
                if cooling_rate < 1 / 8:
                    points_list.append(cooling_point)
                    points_list.append((65, -5))
                    points_list.append((65, 65))
                    points_list.append((-5, 65))
                    points_list.append((-5, -5))
                    points_list.append((30, -5))
                elif cooling_rate < 3 / 8:
                    points_list.append(cooling_point)
                    points_list.append((65, 65))
                    points_list.append((-5, 65))
                    points_list.append((-5, -5))
                    points_list.append((30, -5))
                elif cooling_rate < 5 / 8:
                    points_list.append(cooling_point)
                    points_list.append((-5, 65))
                    points_list.append((-5, -5))
                    points_list.append((30, -5))
                elif cooling_rate < 7 / 8:
                    points_list.append(cooling_point)
                    points_list.append((-5, -5))
                    points_list.append((30, -5))
                else:
                    points_list.append(cooling_point)
                    points_list.append((30, -5))
                pygame.draw.polygon(cooling_surface, (30, 30, 30), points_list)
                cooling_surface.set_alpha(155)
                surface.blit(cooling_surface, (0, 0))
                if cooling > 180:
                    second = cooling_time // 60 + 1
                    font = FontSurface(text=str(second), size=25, color=(255, 255, 200)).surface
                    surface.blit(font, (30 - font.get_width() / 2, 20))

            if self.high_light_time > 0:
                self.high_light_time -= 1
                point_effect = Atlas.load("./data/img/console", "SkillPoint")["defeat"][0][0]
                surface.blit(point_effect, (0, 0))

            if self.mouse_on and self.skill.enabled:
                MessageManager.send_message("cursor_play", "skill")
            if self.skill.skill_using is True:
                using_effect = Atlas.load("./data/img/console", "SkillUsing")["defeat"][0][0]
                surface.blit(using_effect, (0, 0))
            if self.skill.if_auto_use:
                length = self.auto_use_time
                length2 = self.auto_use_time - 30 if self.auto_use_time > 30 else 30 + self.auto_use_time

                pygame.draw.line(surface, (155, 255, 155), (0, 50 - length), (0, 70 - length), 5)
                pygame.draw.line(surface, (155, 255, 155), (length2 - 10, 0), (10 + length2, 0), 5)
                pygame.draw.line(surface, (155, 255, 155), (59, length - 10), (59, 10 + length), 5)
                pygame.draw.line(surface, (155, 255, 155), (50 - length2, 59), (70 - length2, 59), 5)

                self.auto_use_time += 1
                if self.auto_use_time > 60:
                    self.auto_use_time = 0
            if self.skill.enabled is False:
                self.describe = self.base_describe
                self.describe += "&<该技能已禁用>"
                surface = self.skill_ban_surface
                if self.text != self.describe:
                    self.change_text(self.describe)

            self.change_surface(surface, frame=self.frame)

            if self.mouse_right_down is False and pygame.mouse.get_pressed(3)[2] and self.mouse_on:
                self.mouse_right_down = True
                if self.skill.can_auto_use:
                    MessageManager.send_message("change_auto_use", (self.skill.flag.flag, not self.skill.if_auto_use))
            elif pygame.mouse.get_pressed(3)[2] is False:
                self.mouse_right_down = False

    def get_surface(self):
        surface_list = super().get_surface()
        if len(self.resource_require) > 0 and self.mouse_on:
            surface_list.append([self.resource_surface, self.resource_rect])
        return surface_list

    def clear(self):
        super().clear()
        self.skill = None
