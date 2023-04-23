from unit_tools.instruction import Instruction


class MixedInstruction(Instruction):
    def __init__(self, skill, **instructions):
        super().__init__(skill)
        self.instructions = instructions
        self.now_instruction = None

    def change_now_instruction(self, instruction):
        self.now_instruction = instruction
        if instruction is not None:
            instruction.end = False

    def start(self, instructor):
        for i in self.instructions:
            self.instructions[i].start(instructor)
        super().start(instructor)

    def update(self):
        super().update()
        if self.end is False and self.now_instruction is not None:
            self.now_instruction.update()

    def clear(self):
        for i in self.instructions:
            self.instructions[i].clear()
        self.instructions = list()
        self.now_instruction = None
        super().clear()
