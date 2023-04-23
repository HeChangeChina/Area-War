from unit_tools.behavior import Behavior


class ArrayBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.flag.add_flag("array")
        self.icon = "arrayIconS"

    def start(self):
        self.icon_visible = True
        self.name = "列阵"
        self.describe = "周围存在士兵时，该单位受到的伤害减少，造成的伤害增加"
        self.add_attribute_revise("hurt_rate", 0, "array_hurt_rate")
        self.add_attribute_revise("harm_cause_rate", 0, "array_harm_rate")

    def update_15(self):
        soldier_count = 0
        for i in self.unit.radar_list:
            if i.flag.contain_flag("soldier") and i.team == self.unit.team:
                soldier_count += 1
        if soldier_count > 0:
            if soldier_count > 5:
                soldier_count = 5
            self.set_attribute_revise("array_hurt_rate", -soldier_count * 0.06)
            self.set_attribute_revise("array_harm_rate", soldier_count * 0.06)
