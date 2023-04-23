from display.shader import Shader
from auxiliary_tools.flag_manager import FlagManager
from display.atlas import Atlas
from display.animate_controler import AnimateControler
from display.display_object import DisplayObject


class NormalDisplay(DisplayObject):
    def __init__(self, atlas, unit_name, c_rect, fps_level=0, base_event=True):
        super().__init__()
        self.shader = Shader()
        self.atlas = Atlas(atlas, unit_name)
        self.c_rect = c_rect
        self.animate_controler = AnimateControler(self.atlas, self.shader, fps_level)
        self.flag = FlagManager()
        if base_event:
            self.message_require("update_60", self.base_update)

    def base_update(self, data):
        self.animate_controler.animate_update(None)
        self.update()

    def update(self):
        pass

    def get_surface(self):
        return [[self.shader.get_surface(), self.c_rect]]

    def clear(self):
        super().clear()
        self.animate_controler.clear()
        self.if_clear = True
