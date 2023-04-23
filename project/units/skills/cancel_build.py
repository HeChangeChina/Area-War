from unit_tools.skill import Skill
from auxiliary_tools.resources_manager import ResourcesManager


class SkillCancelBuild(Skill):
    def __init__(self, unit, resource_return=0.75, health_require=0):
        super().__init__(unit, target_mode=None)
        self.health_require = health_require
        self.resource_return = resource_return
        self.flag.add_flag("cancel_build")

    def instruction(self, data):
        for i in self.unit.cost:
            ResourcesManager.add_resources(i, self.resource_return * self.unit.cost[i], self.unit.team)
        self.unit.attribute_manager.health = 0
        self.unit.death(self.unit)

    def data_check(self, data):
        return self.unit.attribute_manager.health > self.unit.attribute_manager.get_attribute("max_health") * self.health_require
