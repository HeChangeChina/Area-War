from unit_tools.skill import Skill
from unit_tools.filter import Filter
from units.indicators.move_indicator import MoveIndicator
from auxiliary_tools.message_manager import MessageManager


class SetRallyPoint(Skill):
    def __init__(self, unit):
        super().__init__(unit, Filter(unit, ["unit"], [], [], point=True))
        self.flag.add_flag("move")
        self.draw_time = 1
        if self.unit.flag.contain_flag("production_unit"):
            self.unit.attribute_manager.create_attribute("RallyPoint", self.unit.c_rect.width / 2 + self.unit.c_rect.left)

    def get_instruction(self, data):
        if self.unit.flag.contain_flag("production_unit"):
            point_data = data[0] if type(data) is list else data
            point = data[0] if type(data) is list else data.c_rect.left + data.c_rect.width / 2
            self.unit.attribute_manager.set_attribute("RallyPoint", point_data)
            MessageManager.send_message("add_indicator", MoveIndicator(point))
        return None

    def update(self):
        super().update()
        if self.unit.flag.contain_flag("production_unit") and self.unit.behavior_manager.get("chosen") is not None:
            self.draw_time += 1 if self.draw_time < 21 else -20
            rate = 1 - self.draw_time / 20
            point_data = self.unit.attribute_manager.get_attribute("RallyPoint")
            if point_data is not None:
                center = point_data if type(point_data) is float or type(point_data) is int else \
                    point_data.c_rect.left + point_data.c_rect.width / 2
                MessageManager.send_message("ellipse_draw", [center, 35 * rate, (255, 200, 200), 2, 4.5 * rate])

    def clear(self):
        self.unit.attribute_manager.delete_attribute("production_unit")
        super().clear()
