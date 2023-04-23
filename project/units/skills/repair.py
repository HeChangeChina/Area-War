from unit_tools.skill import Skill
from unit_tools.filter import Filter
from units.instructions.repair import Repair


class RepairSkill(Skill):
    def __init__(self, unit, animate="skill", repair_speed=15):
        super().__init__(unit, Filter(unit, ["unit", "repairable"], ["self"], ["ally", "own"]), can_auto_use=True)
        self.flag.add_flag("repair")
        self.animate = animate
        self.repair_speed = repair_speed

    def distance(self, unit):
        return abs(self.unit.c_rect.left + self.unit.c_rect.width / 2 - unit.c_rect.left - unit.c_rect.width / 2)

    def auto_use_judge(self):
        if self.unit.instructor.waiting:
            for i in self.unit.radar_list:
                if self.target_mode.filter(i) and self.distance(i) < 400 and\
                        i.attribute_manager.health != i.attribute_manager.get_attribute("max_health")\
                        and not i.state_label.contain_flag("under_building"):
                    return i, "clear"
            return False
        else:
            return False

    def get_instruction(self, data):
        if self.data_check(data) is False:
            return None
        return Repair(self, data, self.animate, self.repair_speed)

    def data_check(self, data):
        return not data.state_label.contain_flag("under_building")
