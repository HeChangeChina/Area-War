from unit_tools.effect import Effect
from units.special_effect import SpecialEffect
from auxiliary_tools.message_manager import MessageManager


class CreateSpecialEffect(Effect):
    def take_effect(self, target, trigger):
        if self.data.get("effect_name") is None:
            print("Warning: effect 'CreateSpecialEffect' got the wrong data, 'effect_name' is missing.")
            return
        elif self.data.get("size") is None:
            print("Warning: effect 'CreateSpecialEffect' got the wrong data, 'size' is missing.")
            return
        if self.data.get("follow") is None:
            self.data["follow"] = False
        if self.data.get("fps_level") is None:
            self.data["fps_level"] = 0
        if self.data.get("auto_clear") is None:
            self.data["auto_clear"] = True
        if self.data.get("path") is None:
            self.data["path"] = None
        if self.data.get("index") is None:
            self.data["index"] = 11
        if self.data.get("blend_color") is None:
            self.data["blend_color"] = None
        special_effect = SpecialEffect(self.data["effect_name"], self.data["size"], self.data["follow"],
                                       self.data["fps_level"], self.data["auto_clear"], self.data["path"],
                                       self.data["index"], self.data["blend_color"])
        special_effect.set_follow_obj(target)
        MessageManager.send_message("create_special_effect", special_effect)
        return special_effect
