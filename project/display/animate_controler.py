from base import Base
import random
import pygame


class AnimateControler(Base):
    def __init__(self, atlas, shader, fps_level=0, time_delay=True, base_rotation=0):
        super().__init__()
        self.atlas = atlas
        self.shader = shader
        self.animate_play = "defeat"
        self.surface = self.atlas.atlas_dict[self.animate_play][0][0]
        self.shader.set_surface(pygame.transform.rotate(self.surface, base_rotation))
        self.now_frame = 0
        self.loop_action = "defeat"
        self.defeat_action = "defeat"
        self.now_side = 0
        self.end_recall = None
        self.lock = False
        self.lock_side = False
        self.time_delay = time_delay
        self.rotation = base_rotation
        self.stop = False

        if fps_level == 0:
            self.fps_level = 10
        elif fps_level == 1:
            self.fps_level = 4
        else:
            self.fps_level = 1
        self.now_fps = self.fps_level
        self.animate_speed = 1

    def change_rotation(self, rotation):
        self.rotation = rotation
        self.now_fps = 0
        self.animate_update(None)

    def change_side(self, side):
        if self.lock_side is False:
            self.now_side = side

    def change_defeat_action(self, action):
        self.defeat_action = action

    def return_defeat_action(self):
        self.change_loop_action(self.defeat_action)

    def change_loop_action(self, action):
        if self.lock is False and action != self.loop_action:
            self.animate_play = action
            self.loop_action = action
            self.now_frame = 0
            self.animate_update("")

    def play_action(self, action, end_recall=None, lock=False):
        if self.lock is False:
            self.animate_play = action
            self.now_frame = 0
            self.end_recall = end_recall
            self.lock = lock
            self.now_fps += random.randrange(-4, 4, 1) if self.time_delay else 0
            self.animate_update("")

    def change_animate_frame(self, action):
        if self.lock is False:
            stop = self.stop
            self.stop = False
            self.animate_play = action
            self.now_frame = 0
            self.now_fps = 1
            self.animate_update("")
            self.stop = stop

    def set_animate_frame(self, action, frame):
        self.surface = self.atlas.atlas_dict[action][frame][self.now_side]
        self.now_fps = 0
        self.animate_update("")

    def animate_update(self, data):
        if not self.stop:
            self.now_fps -= self.animate_speed
            while self.now_fps <= 0:
                self.now_fps += self.fps_level
                self.surface = self.atlas.atlas_dict[self.animate_play][self.now_frame][self.now_side]
                if self.rotation == 0:
                    self.shader.set_surface(self.surface)
                else:
                    self.shader.set_surface(pygame.transform.rotate(self.surface, self.rotation))
                if self.now_frame < len(self.atlas.atlas_dict[self.animate_play]) - 1:
                    self.now_frame += 1
                else:
                    if self.end_recall is not None:
                        self.end_recall()
                        self.end_recall = None
                    self.animate_play = self.loop_action
                    self.now_frame = 0
                    self.lock = False
        else:
            self.now_fps -= self.animate_speed
            while self.now_fps <= 0:
                self.now_fps += self.fps_level
                if self.rotation == 0:
                    self.shader.set_surface(self.surface)
                else:
                    self.shader.set_surface(pygame.transform.rotate(self.surface, self.rotation))
