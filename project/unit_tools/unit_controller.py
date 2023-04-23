from base import Base
from unit_tools.filter import Filter


class UnitController(Base):
    def __init__(self, skill_manager, instructor, unit):
        super().__init__()
        self.skill_manager = skill_manager
        self.instructor = instructor
        self.unit = unit
        self.have_weapon = False
        self.movable = False
        self.unit_filter = Filter(unit, excluded_flag=["unit"], required_flag=["unit"])
        self.update_time = 0

    def use_skill(self, skill_flag, data, clear="clear", have_indicator=True, flag_add=None):
        instruction = self.skill_manager.get_instruction_by_flag(skill_flag, data, have_indicator)
        if flag_add is not None:
            instruction.flag.add_flag(flag_add)
        if flag_add == ["auto"] or (self.instructor.now_instruction is not None and
                                    self.instructor.now_instruction.flag.contain_flag("auto")):
            clear = "clear"
        if instruction is not None:
            self.instructor.add_instruction(instruction, clear=clear)

    def replace_skill_instruction(self, skill_flag, data):
        now_instruction = self.skill_manager.get_instruction_by_flag(skill_flag, data)
        before_instruction = self.instructor.get_instruction(self.skill_manager.get(skill_flag))
        if now_instruction is not None:
            self.instructor.replace_instruction(before_instruction, now_instruction)

    def clear_instruction(self):
        self.instructor.clear_instructions()

    def compulsorily_clear_instructions(self):
        self.instructor.compulsorily_clear_instructions()

    def clear(self):
        super().clear()
        self.skill_manager = None
        self.instructor = None
        self.unit = None
        self.unit_filter.clear()
        self.unit_filter = None

    def base_update(self):
        for i in self.skill_manager.skill_list:
            if i.flag.contain_flag("auto_use"):
                use_list = i.auto_use()
                if use_list[0]:
                    self.instructor.add_instruction(i.get_instruction(use_list[1]))

        if self.unit.instructor.now_instruction is None and self.update_time == 0:
            self.update_time = 6
            self.have_weapon = len(self.unit.weapons.weapons) > 0
            self.movable = self.unit.flag.contain_flag("movable_unit")
            if self.have_weapon:
                radar_list = self.unit.radar_list
                self.unit_filter = self.unit.weapons.target_filter
                weapon_range = self.unit.weapons.weapons[0].aim_range
                for i in radar_list:
                    if i.wait_to_death:
                        continue
                    now_range = abs(
                        (i.c_rect.left + i.c_rect.width / 2) - (self.unit.c_rect.left + self.unit.c_rect.width / 2))
                    if self.unit_filter.filter(i) and now_range < 200 + weapon_range:
                        self.use_skill(["skill", "attack"], (self.unit.c_rect.left + self.unit.c_rect.width / 2, 0),
                                       have_indicator=False, flag_add="auto")
        elif self.update_time > 0:
            self.update_time -= 1
        self.update()

    def hurt(self, trigger):
        if self.movable and self.unit.instructor.now_instruction is None:
            target_right = trigger.c_rect.left + trigger.c_rect.width / 2 > self.unit.c_rect.left + self.unit.c_rect.width / 2
            if self.have_weapon:
                target_range = abs(
                    trigger.c_rect.left + trigger.c_rect.width / 2 - self.unit.c_rect.left + self.unit.c_rect.width / 2)
                if target_right:
                    if target_range > 600 or self.unit_filter.filter(trigger) is False or \
                            self.unit.flag.contain_flag("negative_attacker"):
                        self.use_skill(["skill", "move"], (self.unit.c_rect.left + self.unit.c_rect.width / 2 - 100, 0),
                                       have_indicator=False, flag_add="auto")
                    else:
                        self.use_skill(["skill", "attack"], (trigger.c_rect.left + trigger.c_rect.width / 2, 0),
                                       have_indicator=False, flag_add="auto")
                        self.use_skill(["skill", "move"], (self.unit.c_rect.left + self.unit.c_rect.width / 2, 0),
                                       "None", False, flag_add="auto")
                else:
                    if target_range > 600 or self.unit_filter.filter(trigger) is False or \
                            self.unit.flag.contain_flag("negative_attacker"):
                        self.use_skill(["skill", "move"], (self.unit.c_rect.left + self.unit.c_rect.width / 2 + 100, 0),
                                       have_indicator=False, flag_add="auto")
                    else:
                        self.use_skill(["skill", "attack"], (trigger.c_rect.left + trigger.c_rect.width / 2, 0),
                                       have_indicator=False, flag_add="auto")
                        self.use_skill(["skill", "move"], (self.unit.c_rect.left + self.unit.c_rect.width / 2, 0),
                                       "None", False, flag_add="auto")
            else:
                if target_right:
                    self.use_skill(["skill", "move"], (self.unit.c_rect.left + self.unit.c_rect.width / 2 - 100, 0),
                                   have_indicator=False, flag_add="auto")
                else:
                    self.use_skill(["skill", "move"], (self.unit.c_rect.left + self.unit.c_rect.width / 2 + 100, 0),
                                   have_indicator=False, flag_add="auto")

    def update(self):
        pass

