from unit_tools.skill import Skill
from units.instructions.move import Move
from unit_tools.filter import NullFilter
from auxiliary_tools.message_manager import MessageManager
from units.indicators.move_indicator import MoveIndicator


class SkillMove(Skill):
    def __init__(self, unit):
        super().__init__(unit, target_mode=NullFilter(True))
        self.flag.add_flag("move")

    def instruction(self, data):
        if type(data) is tuple or type(data) is list:
            x = data[0]
            if self.have_indicator:
                MessageManager.send_message("add_indicator", MoveIndicator(x))
            return Move(x, self)
        else:
            return Move(data.c_rect.left + data.c_rect.width / 2, self)


