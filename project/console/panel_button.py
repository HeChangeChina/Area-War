from auxiliary_tools.message_manager import MessageManager
from auxiliary_tools.key import Key
from console.console_button import ConsoleButton


class PanelButton(ConsoleButton):
    def __init__(self, c_xy, icon, panel_to, describe="", key=None):
        self.key = key
        super().__init__(c_xy, img=icon, text=describe, frame="PanelButtonFrame", corner=self.key)
        self.panel = panel_to
        if self.key is not None:
            self.key_code = Key.get_code_by_key(self.key)
            self.message_require("key_down", self.key_down)
        else:
            self.key_code = None

    def key_down(self, key):
        if self.key_code == key[0]:
            self.mouse_down()

    def mouse_down(self):
        MessageManager.send_message("panel_to", self.panel)
