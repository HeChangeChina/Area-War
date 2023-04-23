from base import Base
from auxiliary_tools.flag_manager import FlagManager


class Instruction(Base):
    def __init__(self, skill):
        super().__init__()
        self.instructor = None
        self.removable = True
        self.end = False
        self.skill = skill
        self.if_finish = False
        self.additional = False
        self.flag = FlagManager()
        self.flag.add_flag("instruction")

    def draw(self):
        pass

    def update(self):
        if self.end is False:
            self.update_()

    def update_(self):
        pass

    def start(self, instructor):
        if self.skill.before_use_check():
            self.instructor = instructor
            self.start_()
        else:
            self.end = True

    def start_(self):
        pass

    def clear(self):
        if self.skill is not None:
            if self.if_finish:
                self.skill.finish()
            else:
                self.skill.cancel()
            self.skill = None
        if self.instructor is not None:
            self.instructor.reset_push()
            self.instructor.animate_speed(1)
            self.instructor = None
        self.end = True
        super().clear()
