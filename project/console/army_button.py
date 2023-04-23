from display.display_object import DisplayObject
from auxiliary_tools.key_listener import KeyListener
from unit_tools.team_manager import TeamManager
from display.atlas import Atlas
from display.font import FontSurface
from auxiliary_tools.message_manager import MessageManager
from pygame import Surface
from pygame import Rect
from pygame import K_LSHIFT
from pygame import K_LCTRL


class ArmyButton(DisplayObject):
    def __init__(self, y, key, unit_controller, str_key="0"):
        super().__init__()
        self.key = key
        self.surface = Surface((100, 50))
        self.c_rect = Rect(0, y, 100, 50)
        self.unit_controller = unit_controller
        self.atlas = Atlas.load("./data/img/console", "ArmyButton")
        self.text = FontSurface(text=str_key, size=20).surface

        self.units = list()
        self.key_frame = 2
        self.units_count = -1
        self.double_click_frame = 0

        self.message_require("key_down", self.key_down)
        self.message_require("update_6", self.units_update)
        self.message_require("update_60", self.graph_update)

        self.graph_update(None)

    def graph_update(self, data):
        self.key_frame -= 1 if self.key_frame > 0 else 0
        self.double_click_frame -= 1 if self.double_click_frame > 0 else 0
        if self.key_frame == 1 or self.key_frame == 7 or self.units_count != len(self.units):
            surface = Surface((100, 50))
            surface.set_colorkey((0, 0, 0))
            bg = "defeat" if self.key_frame == 0 or self.key_frame == 1 else "push"
            surface.blit(self.atlas[bg][0][0], (0, 0))
            surface.blit(self.text, (5, 15))

            if len(self.units) > 0:
                icon = self.units[0].unit_panel["unit_icon"]
                icon_surface = Atlas.load("./data/img/units_icon", icon)["defeat"][0][0]
                surface.blit(icon_surface, (10, 0))

                text = FontSurface(text=str(len(self.units)), size=20).surface
                text_height = text.get_height()
                surface.blit(text, (55, 25 - text_height / 2))
            self.surface = surface

    def get_surface(self):
        return [self.surface, self.c_rect]

    def units_update(self, data):
        for i in self.units:
            if i.wait_to_death:
                self.units.remove(i)

    def key_down(self, data):
        if data[0] == self.key and self.unit_controller is not None:
            if self.double_click_frame > 0 and len(self.units) > 0:
                MessageManager.send_message("focus_on", self.units[0])
                return
            self.key_frame = 8
            self.double_click_frame = 10
            if KeyListener.get_key(K_LSHIFT):
                for i in self.unit_controller.unit_list:
                    if i not in self.units and TeamManager.is_player(i.team):
                        self.units.append(i)
            elif KeyListener.get_key(K_LCTRL):
                if len(self.unit_controller.unit_list) > 0 and \
                        TeamManager.is_player(self.unit_controller.unit_list[0].team):
                    self.units = self.unit_controller.unit_list
            else:
                if len(self.units) == 0:
                    return
                self.unit_controller.set_units(self.units)

    def clear(self):
        self.unit_controller = None
        self.units = list()
        super().clear()
