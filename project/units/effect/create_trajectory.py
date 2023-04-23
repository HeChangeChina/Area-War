from unit_tools.effect import Effect
from units.trajectory import Trajectory
from auxiliary_tools.message_manager import MessageManager


# 这个效果已被废除使用
class CreateTrajectory(Effect):
    def take_effect(self, target, trigger):
        if self.data.get("name") is None:
            print("Warning: effect 'CreateSpecialEffect' got the wrong data, 'name' is missing.")
            return
        elif self.data.get("size") is None:
            print("Warning: effect 'CreateSpecialEffect' got the wrong data, 'size' is missing.")
            return
        if self.data.get("fps_level") is None:
            self.data["fps_level"] = 1

        trajectory = Trajectory(self.data["effect_name"], self.data["size"], self.data["fps_level"])

        MessageManager.send_message("create_trajectory", trajectory)
