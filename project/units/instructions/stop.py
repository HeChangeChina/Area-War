from unit_tools.instruction import Instruction


class Stop(Instruction):
    def __init__(self, skill):
        super().__init__(skill)
        self.additional = True

    def start_(self):
        self.instructor.clear_instructions()
        self.instructor.animate_loop("defeat")
        self.if_finish = True
        self.end = True
