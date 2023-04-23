from base import Base
from auxiliary_tools.flag_manager import FlagManager
import pygame


class DisplayObject(Base):
    def __init__(self):
        super().__init__()
        self.flag = FlagManager()
        self.in_screen = False
        self.visible = True
        self.if_clear = False
        self.mouse_enabled = False
        self.c_rect = pygame.Rect(0, 0, 0, 0)

    def mouse_in(self):
        pass

    def mouse_out(self):
        pass

    def mouse_down(self):
        pass

    def mouse_up(self):
        pass

    def mouse_click(self):
        pass

    def clear(self):
        super().clear()
        self.visible = False
        self.if_clear = True

    def get_surface(self):
        pass
