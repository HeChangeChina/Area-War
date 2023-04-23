from unit_tools.skill import Skill
from unit_tools.filter import NullFilter
from units.instructions.attack import AttackTarget
from units.instructions.attack import HoldAttackTarget
from units.instructions.advance import Advance
from units.instructions.advance import HoldAdvance
from units.indicators.attack_indicator import AttackIndicator
from units.behaviors.be_attacked import BeAttacked
from auxiliary_tools.message_manager import MessageManager


class SkillAttack(Skill):
    def __init__(self, unit):
        super().__init__(unit=unit, target_mode=None, animate="attack")
        self.flag.add_flag("attack")
        self.weapons = unit.weapons
        self.target_mode = self.weapons.target_filter
        if self.target_mode is None:
            self.target_mode = NullFilter(False)
        else:
            self.target_mode.point = True

    def instruction(self, data):
        if type(data) is not list and type(data) is not tuple:
            x = data.c_rect.left + data.c_rect.width / 2
            if self.have_indicator:
                MessageManager.send_message("add_indicator", AttackIndicator(x))
                data.behavior_manager.add(BeAttacked())
            if self.unit.flag.contain_flag("movable_unit"):
                return AttackTarget(self, self.weapons, data)
            elif self.unit.flag.contain_flag("building"):
                return HoldAttackTarget(self, self.weapons, data)
        else:
            x = data[0]
            if self.have_indicator:
                MessageManager.send_message("add_indicator", AttackIndicator(x))
            if self.unit.flag.contain_flag("movable_unit"):
                return Advance(self, self.weapons, x)
            elif self.unit.flag.contain_flag("building"):
                return HoldAdvance(self, self.weapons, x)
        return None

    def update(self):
        super().update()
        if self.target_mode != self.weapons.target_filter:
            self.target_mode = self.weapons.target_filter

    def clear(self):
        super().clear()
        self.weapons = None
        self.target_mode = None
