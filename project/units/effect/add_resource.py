from unit_tools.effect import Effect
from auxiliary_tools.resources_manager import ResourcesManager


class AddResource(Effect):
    def effect(self, target, trigger):
        if self.data.get("resource_type") is None:
            print("Warning: effect 'add_behavior' got the wrong data, 'behavior' is missing.")
            return
        if self.data.get("value") is None:
            print("Warning: effect 'add_behavior' got the wrong data, 'behavior' is missing.")
            return
        ResourcesManager.add_resources(self.data["resource_type"], self.data["value"], trigger.team)
