from unit_tools.instruction import Instruction
from auxiliary_tools.message_manager import MessageManager


class ApproachAndUse(Instruction):
    def __init__(self, skill, target, chant_frame, chant_animate, skill_advance, skill_animate, aiming_range,
                 escape_range, chant_stoppable, pre_effect):
        super().__init__(skill)
        self.flag.add_flag("approach_and_use")

        self.target = target
        self.skill_advance = skill_advance
        self.total_frame = chant_frame
        self.chant_animate = chant_animate
        self.skill_animate = skill_animate
        self.chant_frame = chant_frame - self.skill_advance
        self.aiming_range = aiming_range
        self.escape_range = escape_range
        self.chant_stoppable = chant_stoppable
        self.pre_effect = pre_effect

        self.aiming = False
        self.skill_animate_play = False
        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.target.c_rect.left + self.target.c_rect.width / 2 \
            if type(self.target) is not list and type(self.target) is not tuple else self.target[0]
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (60, 60, 255), 2, 4 * rate])

    def start_(self):
        self.instructor.add_label("no_pushing")
        if self.instructor.contain_flag("movable_unit") is False and self.instructor.in_distance(
                self.target.c_rect.left + self.target.c_rect.width / 2, self.aiming_range) is False:
            self.end = True
        else:
            self.instructor.animate_loop("walk")

    def update_(self):
        if self.aiming is False and type(self.target) is not list and type(self.target) is not tuple and \
                self.target.state_label.contain_flag(["hidden", "invincible"]):
            self.end = True
            return
        else:
            if type(self.target) is list or type(self.target) is tuple:
                target_x = self.target[0]
            else:
                target_x = self.target.c_rect.left + self.target.c_rect.width / 2

            if self.aiming is False:
                if self.instructor.approach(target_x, self.aiming_range):
                    if self.skill.before_take_effect_check():
                        if self.pre_effect is not None:
                            self.pre_effect.take_effect(self.target, self.instructor.unit)
                        self.aiming = True
                        self.instructor.animate_loop(self.chant_animate)
                        self.instructor.remove_label("no_pushing")
                    else:
                        self.end = True
                        self.instructor.remove_label("no_pushing")
                        return
            else:
                self.removable = self.chant_stoppable
                self.chant_frame -= 1 if self.chant_frame > 0 else 0
                if self.chant_frame <= 0:
                    if abs(target_x - self.instructor.c_rect().left - self.instructor.c_rect().width / 2) > \
                            self.escape_range + self.aiming_range:
                        self.end = True
                        return

                    if self.skill_animate_play is False:
                        self.skill_animate_play = True
                        self.instructor.animate_play(self.skill_animate)

                    self.skill_advance -= 1 if self.skill_advance > 0 else 0
                    if self.skill_advance <= 0:
                        effect = self.skill.take_effect()
                        effect.take_effect(self.target, self.skill.unit)
                        self.end = True
                        self.if_finish = True
                        return

                if self.total_frame >= 60:
                    hm_bar = self.instructor.get_hm_bar()
                    if hm_bar is not None:
                        chant_rate = (self.total_frame - self.skill_advance - self.chant_frame) / self.total_frame \
                            if self.total_frame - self.skill_advance - self.chant_frame > 0 else 0
                        hm_bar.chant_bar = chant_rate

    def clear(self):
        if self.instructor is not None:
            hm_bar = self.instructor.get_hm_bar()
            if hm_bar is not None:
                hm_bar.chant_bar = 0
            self.instructor.remove_label("no_pushing")
        super().clear()
        self.target = None

