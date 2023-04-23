from base import Base
from auxiliary_tools.flag_manager import FlagManager
from auxiliary_tools.tech_tree import TechTree
from unit_tools.effect import Effect


class Skill(Base):
    def __init__(self, unit, target_mode, quick_spell=True, cooling=0, effect=Effect(),
                 animate="skill", can_auto_use=False, magic_require=0, sight=None,
                 tech_require=None, tech_mode="have"):
        super().__init__()
        self.unit = unit
        self.flag = FlagManager()
        self.flag.add_flag("skill")
        self.target_mode = target_mode
        self.quick_spell = quick_spell
        self.cooling = cooling
        self.effect = effect
        self.animate = animate
        self.can_auto_use = can_auto_use
        self.if_auto_use = can_auto_use
        self.magic_require = magic_require
        self.resource_use = 0
        self.sight = sight

        self.resource_cost_show = dict()
        self.cooling_time = 0
        self.instruction_count = 0
        self.if_ready = True
        self.enabled = True
        self.instruction_replaceable = False
        self.skill_using = False
        self.magic_ample = False
        self.have_indicator = True

        self.tech_require = tech_require
        self.tech_mode = tech_mode
        if self.tech_require is not None:
            if self.tech_mode == "have":
                self.enabled = TechTree.have_tech(self.unit.team, self.tech_require)
            else:
                self.enabled = not TechTree.have_tech(self.unit.team, self.tech_require)

    def resource_ample(self):
        return self.magic_ample

    def finish(self):
        self.skill_using = False
        self.instruction_count -= 1

    def cancel(self):
        self.skill_using = False
        self.instruction_count -= 1

    def get_instruction(self, data):
        self.instruction_count += 1
        return self.instruction(data)

    def data_check(self, data):
        return True

    def instruction(self, data):
        pass

    def before_use_check(self):
        if self.if_ready is False:
            return False
        if self.before_use_check_else() is False:
            return False
        self.skill_using = True
        return True

    def before_use_check_else(self):
        return True

    def auto_use(self):
        if self.if_ready is False or self.if_auto_use is False:
            return False
        else:
            return self.auto_use_judge()

    def auto_use_judge(self):
        return False

    def take_effect(self):
        if self.before_take_effect_check():
            if self.magic_require > 0:
                self.unit.attribute_manager.magic_use(self.magic_require)
            self.cooling_time = int(self.cooling * 60)
            self.if_ready = False
            return self.effect
        else:
            return None

    def before_take_effect_check(self):
        if self.unit.attribute_manager.magic < self.magic_require:
            return False
        if self.before_take_effect_check_else() is False:
            return False
        return True

    def before_take_effect_check_else(self):
        return True

    def update(self):
        if self.tech_require is not None:
            if type(self.tech_require) is tuple:
                enabled = True
                for i in range(len(self.tech_require)):
                    if self.tech_mode[i] == "have":
                        if not TechTree.have_tech(self.unit.team, self.tech_require[i]):
                            enabled = False
                            break
                    else:
                        if TechTree.have_tech(self.unit.team, self.tech_require[i]):
                            enabled = False
                            break
                self.enabled = enabled
            else:
                if self.tech_mode == "have":
                    self.enabled = TechTree.have_tech(self.unit.team, self.tech_require)
                else:
                    self.enabled = not TechTree.have_tech(self.unit.team, self.tech_require)

        if self.cooling_time > 0:
            self.cooling_time -= 1
            self.if_ready = False
        else:
            self.if_ready = True
        if self.enabled is False:
            self.if_ready = False
        if self.unit.attribute_manager.magic < self.magic_require:
            self.magic_ample = False
            self.if_ready = False
        else:
            self.magic_ample = True

    def clear(self):
        super().clear()
        self.unit = None
        if self.target_mode is not None:
            self.target_mode.clear()
