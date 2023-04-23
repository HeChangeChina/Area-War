import pygame
from display.normal_display import NormalDisplay


class Cursor(NormalDisplay):
    def __init__(self):
        super().__init__("./data/img/cursor", "cursor", pygame.Rect(-25, -25, 50, 50), 2)
        self.cursor_style = "defeat"
        self.cursor_style_now = "defeat"
        self.side = 0
        self.if_lock = False
        self.animate_controler.time_delay = False

        pygame.mouse.set_visible(False)

        self.message_require("cursor_set", self.m_set_style)
        self.message_require("cursor_play", self.m_play_style)
        self.message_require("stop_update_60", self.base_update)

    def lock(self):
        self.if_lock = True

    def unlock(self):
        self.if_lock = False

    def m_set_style(self, data):
        if type(data) is not list:
            self.set_style(data)

    def m_play_style(self, data):
        if type(data) is not list:
            self.play_style(data)

    def set_style(self, style):
        if self.if_lock is False:
            self.cursor_style = style
            self.animate_controler.change_loop_action(style)

    def play_style(self, style):
        if self.if_lock is False:
            self.animate_controler.play_action(style)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.c_rect.left = mouse_x - 25
        self.c_rect.top = mouse_y - 25

        self.cursor_style_now = self.animate_controler.animate_play
        """
        if pygame.mouse.get_pressed(3)[0] and self.cursor_style == "defeat" and \
                (self.cursor_style_now == "defeat" or "down"):
            self.play_style("down")
        """
