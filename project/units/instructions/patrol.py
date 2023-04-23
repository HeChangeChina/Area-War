from units.mixed_instruction import MixedInstruction
from units.instructions.advance import Advance
from units.skills.null_skill import NullSkill
from unit_tools.instruction import Instruction
from auxiliary_tools.message_manager import MessageManager


class Patrol(MixedInstruction):
    def __init__(self, skill, weapons, target_x):
        super().__init__(skill, attack=Advance(NullSkill(), weapons, target_x))
        self.flag.add_flag("stoppable")
        self.target_x = target_x
        self.start_x = 0
        self.target = 1

        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        target = self.target_x + self.instructor.c_rect().width / 2
        MessageManager.send_message("ellipse_draw", [target, 20 * rate, (80, 150, 150), 2, 4 * rate])
        MessageManager.send_message("ellipse_draw", [self.start_x, 20 * rate, (80, 150, 150), 2, 4 * rate])

    def start_(self):
        self.start_x = self.instructor.c_rect().left + self.instructor.c_rect().width / 2
        self.instructions["attack"].target = self.target_x
        self.change_now_instruction(self.instructions["attack"])
        self.instructor.add_instruction(Instruction(None), clear="None")

    def update_(self):
        if self.now_instruction.end:
            if self.target == 0:
                self.target = 1
                attack_ins = Advance(NullSkill(), self.instructions["attack"].weapons, self.target_x)
                attack_ins.start(self.instructor)
                self.instructions["attack"].clear()
                self.instructions["attack"] = attack_ins
            elif self.target == 1:
                self.target = 0
                attack_ins = Advance(NullSkill(), self.instructions["attack"].weapons, self.start_x)
                attack_ins.start(self.instructor)
                self.instructions["attack"].clear()
                self.instructions["attack"] = attack_ins
            self.change_now_instruction(self.instructions["attack"])
