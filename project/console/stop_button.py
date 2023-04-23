from display.display_object import DisplayObject
from display.atlas import Atlas
from auxiliary_tools.message_manager import MessageManager
import pygame


class StopButton(DisplayObject):
    def __init__(self):
        super().__init__()

        self.atlas = Atlas.load("./data/img/console", "StopButton")
        self.surface = self.atlas["stop"][0][0]
        self.c_rect = pygame.Rect(1840, 0, 80, 80)

        self.mouse_on = False
        self.if_stop = False

        self.mouse_enabled = True

        self.message_require("update_60", self.update)
        self.message_require("stop_update_60", self.update)

    def get_surface(self):
        return [[self.surface, self.c_rect]]

    def mouse_in(self):
        self.mouse_on = True

    def mouse_out(self):
        self.mouse_on = False

    def mouse_click(self):
        self.if_stop = not self.if_stop
        MessageManager.send_message("game_stop", None)

    def update(self, data):
        if self.if_stop:
            self.surface = self.atlas["continueM"][0][0] if self.mouse_on else self.atlas["continue"][0][0]
        else:
            self.surface = self.atlas["stopM"][0][0] if self.mouse_on else self.atlas["stop"][0][0]
