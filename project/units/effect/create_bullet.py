from unit_tools.effect import Effect
from auxiliary_tools.message_manager import MessageManager


class CreateBullet(Effect):
    def take_effect(self, target, trigger):
        if self.data.get("bullet") is None:
            print("Warning: effect 'CreateBullet' got the wrong data, 'bullet' is missing.")
            return
        bullet = self.data["bullet"].get_bullet()
        bullet.start(target, trigger)
        MessageManager.send_message("create_bullet", bullet)
