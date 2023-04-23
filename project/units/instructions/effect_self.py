from unit_tools.instruction import Instruction


class EffectSelfAdditional(Instruction):
    def __init__(self, skill):
        super().__init__(skill)
        self.additional = True

    def start_(self):
        effect = self.skill.take_effect()
        if effect is not None:
            self.instructor.effect(effect)
        self.if_finish = True
        self.end = True

