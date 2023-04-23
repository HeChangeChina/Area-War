from console.console_button import ConsoleButton
from display.font import FontSurface
from display.atlas import Atlas
from pygame import Surface
from auxiliary_tools.message_manager import MessageManager


class UnitProductionButton(ConsoleButton):
    def __init__(self, x, y, unit_icon, production_manager, number):
        super().__init__([x, y], frame="ProductionFrame", size=(50, 50))
        self.production_manager = production_manager
        self.index = number
        self.icon = None
        self.number = str(number + 1)
        self.controllable = True
        self.change_unit(unit_icon)

    def change_unit(self, icon):
        self.icon = icon
        surface = Surface((50, 50))
        surface.fill((160, 130, 110))
        if icon is None:
            font_surface = FontSurface(self.number, size=25, color=(210, 180, 150)).surface
            left = (50 - font_surface.get_width()) / 2
            top = (50 - font_surface.get_height()) / 2
            surface.blit(font_surface, (left, top))
        else:
            unit_surface = Atlas.load("./data/img/units_icon", icon)["defeat"][0][0]
            surface.blit(unit_surface, (0, 0))
        self.change_surface(surface, "ProductionFrame")

    def update(self):
        super().update()
        if self.mouse_on and self.icon is not None and self.controllable:
            cursor = "chooseDefeat"
            MessageManager.send_message("cursor_play", cursor)

    def button_down(self, index):
        pass

    def mouse_down(self):
        if self.controllable and self.icon is not None:
            self.production_manager.button_down(self.index)

    def clear(self):
        self.production_manager = None
        super().clear()
