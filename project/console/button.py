from display.normal_display import NormalDisplay
from pygame import Rect
from display.font import FontSurface
from auxiliary_tools.message_manager import MessageManager


class Button(NormalDisplay):
    def __init__(self, x, y, text, message):
        super().__init__("./data/img/console", "button", Rect(x, y, 200, 70))
        self.text_surface = FontSurface(size=18, text=text, color=(255, 235, 200)).surface
        self.text_rect = Rect(x + 100 - self.text_surface.get_width() / 2, y + 26, 0, 0)
        self.message = message
        self.mouse_enabled = True

    def get_surface(self):
        surface_list = super().get_surface()
        surface_list.append([self.text_surface, self.text_rect])
        return surface_list

    def mouse_click(self):
        MessageManager.send_message(self.message, None)

    def mouse_in(self):
        MessageManager.send_message("cursor_set", "skill")

    def mouse_out(self):
        MessageManager.send_message("cursor_set", "defeat")
        self.animate_controler.change_loop_action("defeat")

    def mouse_down(self):
        self.animate_controler.change_loop_action("press")

    def mouse_up(self):
        self.animate_controler.change_loop_action("defeat")
