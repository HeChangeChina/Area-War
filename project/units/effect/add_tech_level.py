from unit_tools.effect import Effect
from auxiliary_tools.tech_tree import TechTree


class AddTechLevel(Effect):
    def effect(self, target, trigger):
        if self.data.get("tech") is None:
            print("Warning: effect 'add_behavior' got the wrong data, 'behavior' is missing.")
            return
        if self.data.get("level") is None:
            self.data["level"] = 1
        TechTree.add_level(self.data["tech"], trigger.team, self.data["level"])
