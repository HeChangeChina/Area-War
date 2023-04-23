from unit_tools.instruction import Instruction


class Flash(Instruction):
    def __init__(self, skill, target, length):
        self.target = target
        self.length = length
        super().__init__(skill)

    def start_(self):
        self_x = self.instructor.c_rect().left + self.instructor.c_rect().width / 2
        self_y = self.instructor.c_rect().top + self.instructor.c_rect().height / 2
        out_of_range = abs(self.target - self_x) > self.length
        if self_x > self.target and out_of_range:
            self.target = self_x - self.length
        elif self_x < self.target and out_of_range:
            self.target = self_x + self.length
        effect = self.skill.take_effect()
        effect.take_effect((self_x, self_y), self.instructor.unit)
        effect.take_effect((self.target, self_y), self.instructor.unit)
        self.instructor.set_x(self.target)
        self.end = True
        self.if_finish = True
