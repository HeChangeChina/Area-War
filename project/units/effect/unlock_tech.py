from unit_tools.effect import Effect
from auxiliary_tools.tech_tree import TechTree


class UnlockTech(Effect):
    def effect(self, target, trigger):
        if self.data.get("tech") is None:
            print("Warning: effect 'add_behavior' got the wrong data, 'behavior' is missing.")
            return
        TechTree.set_level(self.data["tech"], trigger.team, 1)
