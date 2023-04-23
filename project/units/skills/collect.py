from unit_tools.skill import Skill
from unit_tools.filter import Filter
from units.instructions.collect import Collect


class CollectSkill(Skill):
    def __init__(self, unit, animate="defeat", collect_sped=2):
        super().__init__(unit, Filter(unit, [], ["enemy"], ["storehouse", "resource"]))
        self.flag.add_flag("collect")

        self.animate = animate
        self.collect_speed = collect_sped

        if unit.attribute_manager.get_attribute("resource_carry") is None:
            unit.attribute_manager.create_attribute("resource_carry", ["wood", 0])
        if unit.attribute_manager.get_attribute("resource_carry_limit") is None:
            unit.attribute_manager.create_attribute("resource_carry_limit", 15)

    def instruction(self, data):
        if data.flag.contain_flag("resource"):
            return Collect(self, self.animate, self.collect_speed, target=data)
        else:
            return Collect(self, self.animate, self.collect_speed, storehouse=data)
