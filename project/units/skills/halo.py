from unit_tools.skill import Skill


class Halo(Skill):
    def __init__(self, unit, unit_filter, flag, influence_range=600, effect=None, tech_require=None, tech_mode="have"):
        super().__init__(unit, target_mode=None, effect=effect, tech_require=tech_require, tech_mode=tech_mode)
        self.flag.add_flag(flag)
        self.unit_filter = unit_filter
        self.influence_range = influence_range
        self.cycle = 6

    def update(self):
        super().update()
        if self.unit.state_label.contain_flag("under_building"):
            return
        self.cycle -= 1 if self.cycle > 0 else 0
        if self.enabled and self.cycle == 0:
            self.cycle = 6
            if self.unit_filter.filter(self.unit):
                self.effect.take_effect(self.unit, self.unit)
            for i in self.unit.radar_list:
                distance = abs(i.c_rect.left - self.unit.c_rect.left + i.c_rect.width / 2 - self.unit.c_rect.width / 2)
                if self.unit_filter.filter(i) and distance <= self.influence_range:
                    self.effect.take_effect(i, self.unit)

    def clear(self):
        self.unit_filter.clear()
        super().clear()


