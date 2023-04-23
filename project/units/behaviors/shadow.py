from unit_tools.behavior import Behavior
from auxiliary_tools.message_manager import MessageManager


class Shadow(Behavior):
    def __init__(self, shadow_size=18, c_x=0):
        super().__init__()
        self.flag.add_flag(["shadow"])
        self.unit = None
        self.unit_rect = None
        self.c_x = c_x
        self.shadow_size = shadow_size
        # self.at_dict = Atlas.load("./data/img/behaviors/HMBar", "hmbframe")

    def start(self):
        self.update_60()

    def update_60(self):
        if self.unit.state_label.contain_flag("hidden") or self.unit.state_label.contain_flag("in_fog"):
            return

        self.unit = self.manager.unit
        self.unit_rect = self.unit.c_rect

        center = self.unit_rect.left + self.unit_rect.width / 2 + self.c_x
        MessageManager.send_message("shadow_draw", [center, self.shadow_size])

    def clear(self):
        super().clear()
        self.unit = None
        self.unit_rect = None
