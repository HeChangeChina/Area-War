from unit_tools.behavior import Behavior
from auxiliary_tools.message_manager import MessageManager


class BeAttacked(Behavior):
    def __init__(self):
        super().__init__()
        self.last_frame = 40
        self.flag.add_flag("be_attacked")

    def update_60(self):
        center = self.unit.c_rect.left + self.unit.c_rect.width / 2
        rate = self.last_frame / 20 if self.last_frame > 20 else 1
        color = (150, 80, 80)
        MessageManager.send_message("ellipse_draw", [center, self.unit.volume * rate, color, 1])
