from display.normal_display import NormalDisplay
from auxiliary_tools.exact_rect import ERect
from auxiliary_tools.ballistic import Ballistic
from units.trajectory import Trajectory
from random import random
import math
import pygame


class Bullet(NormalDisplay):
    def __init__(self, name, effect, speed=600, last_time=20, direct=True, ballistic=Ballistic(), trajectory_name=None,
                 trajectory_size=None, trajectory_fps=1, trajectory_cycle=2, trajectory_shift=5, hit_effect=None,
                 fps_level=0, start_shifting=(0, 0)):
        e_rect = ERect()
        self.target = None
        self.trigger = None
        self.effect = effect
        self.speed = speed / 60
        self.last_time = last_time * 60
        self.direct = direct
        self.ballistic = ballistic
        self.if_start = 2
        super().__init__("./data/img/bullet/" + name, name, e_rect, base_event=False, fps_level=fps_level)
        self.c_rect.width = self.shader.op_surface.get_width()
        self.c_rect.height = self.shader.op_surface.get_height()

        self.trajectory_name = trajectory_name
        self.trajectory_size = trajectory_size
        self.trajectory_fps = trajectory_fps
        self.trajectory_cycle = trajectory_cycle
        self.trajectory_shift = trajectory_shift
        self.trajectory_time = trajectory_cycle

        self.hit_effect = hit_effect

        self.random_d = [0, 0]
        self.start_point = [0, 0]
        self.start_shifting = start_shifting

    def start(self, target, trigger):
        if self.start_shifting == (0, 0):
            self.c_rect.left = trigger.c_rect.left + trigger.c_rect.width / 2 - self.c_rect.width / 2 + \
                               trigger.bullet_anchor[0]
            self.c_rect.top = trigger.c_rect.top + trigger.c_rect.height / 2 - self.c_rect.height / 2 + \
                              trigger.bullet_anchor[1]
        else:
            self.c_rect.left = trigger.c_rect.left + trigger.c_rect.width / 2 - self.c_rect.width / 2 + \
                               self.start_shifting[0]
            self.c_rect.top = trigger.c_rect.top + trigger.c_rect.height / 2 - self.c_rect.height / 2 + \
                               self.start_shifting[1]

        self.target = target
        self.trigger = trigger
        move = self.calculate()
        if self.direct is False:
            move["angle"] = 0
        self.start_point[0] = self.c_rect.left + self.c_rect.width / 2
        self.start_point[1] = self.c_rect.top + self.c_rect.height / 2
        self.animate_controler.change_rotation(move["angle"])
        self.message_require("update_60", self.base_update)

        if not (type(self.target) is list or type(self.target) is tuple):
            length = target.volume * random()
            angle = math.pi * 2 * random()
            self.random_d[0] = length * math.cos(angle)
            self.random_d[1] = length * math.sin(angle) * 0.6
            self.random_d[1] += target.volume * 0.7 if target.flag.contain_flag("building") else 0

    def calculate(self):
        if type(self.target) is list or type(self.target) is tuple:
            center_x = self.target[0]
            center_y = self.target[1]
        else:
            center_x = self.target.c_rect.left + self.target.c_rect.width / 2 + self.random_d[0]
            center_y = self.target.c_rect.top + self.target.c_rect.height / 2 + self.random_d[1]
        self_x = self.c_rect.left + self.c_rect.width / 2
        self_y = self.c_rect.top + self.c_rect.height / 2
        ballistic = self.ballistic.calculate(self.speed, (self_x, self_y), (center_x, center_y), self.c_rect.width / 2,
                                             self.start_point, self.if_start > 0)
        self.if_start -= 1 if self.if_start > 0 else 0
        return ballistic

    def update(self):
        move = self.calculate()
        if move["arrive"]:
            self.effect.take_effect(self.target, self.trigger)
            if self.hit_effect is not None:
                if type(self.target) is tuple or type(self.target) is list:
                    center_x = self.target[0]
                    center_y = self.target[1]
                else:
                    center_x = self.target.c_rect.left + self.target.c_rect.width / 2 + self.random_d[0]
                    center_y = self.target.c_rect.top + self.target.c_rect.height / 2 + self.random_d[1]
                self.hit_effect.take_effect((center_x, center_y), self.trigger)
            self.clear()
        else:
            self.c_rect.left += move["move"][0]
            self.c_rect.top += move["move"][1]
        if self.direct:
            self.animate_controler.rotation = move["angle"]
        self.last_time -= 1
        if self.last_time < 0:
            self.clear()

        if self.trajectory_name is not None:
            if self.trajectory_time > 0:
                self.trajectory_time -= 1
            else:
                self.trajectory_time = self.trajectory_cycle
                center_x = self.c_rect.left + self.c_rect.width / 2
                center_y = self.c_rect.top + self.c_rect.height / 2

                x_rate = move["move"][0] / self.speed
                y_rate = move["move"][1] / self.speed

                center_x -= x_rate * self.trajectory_shift
                center_y -= y_rate * self.trajectory_shift

                c_rect = pygame.Rect(center_x - self.trajectory_size[0] / 2, center_y - self.trajectory_size[1] / 2,
                                     self.trajectory_size[0], self.trajectory_size[1])
                trajectory = Trajectory(self.trajectory_name, c_rect, self.trajectory_fps)

    def clear(self):
        super().clear()
        self.target = None
        self.trigger = None
