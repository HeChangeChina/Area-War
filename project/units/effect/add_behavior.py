from unit_tools.effect import Effect
from copy import copy


class AddBehavior(Effect):
    def effect(self, target, trigger):
        if self.data.get("behavior") is None:
            print("Warning: effect 'add_behavior' got the wrong data, 'behavior' is missing.")
            return
        target.behavior_manager.add(copy(self.data["behavior"]))
