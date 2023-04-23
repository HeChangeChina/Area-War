from unit_tools.instruction import Instruction
from auxiliary_tools.message_manager import MessageManager


class Move(Instruction):
    def __init__(self, target, skill):
        super().__init__(skill)
        self.flag.add_flag("move")
        self.target = target
        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        MessageManager.send_message("ellipse_draw", [self.target, 15 * rate, (255, 255, 255), 2, 4 * rate])

    def start_(self):
        if self.skill.before_take_effect_check():
            self.skill.take_effect()
        self.instructor.add_label("no_pushing")
        if self.instructor.get_loop_action() != "walk" or self.instructor.get_animate_play() != "walk":
            self.instructor.animate_loop("walk")

    def update_(self):
        self.instructor.add_label("no_pushing")
        self.end = self.instructor.approach(self.target)
        self.instructor.animate_speed(self.instructor.attribute("speed_rate"))
        if self.end:
            self.if_finish = True

    def clear(self):
        if self.instructor is not None:
            self.instructor.remove_label("no_pushing")
        super().clear()
