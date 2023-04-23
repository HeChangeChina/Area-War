from display.normal_display import NormalDisplay
from auxiliary_tools.message_manager import MessageManager


class Trajectory(NormalDisplay):
    def __init__(self, name, c_rect, fps_level=1):
        super().__init__("./data/img/trajectory/" + name, name, c_rect, fps_level=fps_level)
        self.animate_controler.play_action("defeat", end_recall=self.clear, lock=True)
        MessageManager.send_message("create_trajectory", self)
