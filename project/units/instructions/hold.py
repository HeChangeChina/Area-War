from units.mixed_instruction import MixedInstruction
from units.instructions.attack import HoldAttackTarget
from units.skills.null_skill import NullSkill
from auxiliary_tools.message_manager import MessageManager


class Hold(MixedInstruction):
    def __init__(self, skill, weapons):
        super().__init__(skill, attack=HoldAttackTarget(NullSkill(), weapons, None))
        self.flag.add_flag("stoppable")
        self.lock_target = None
        self.weapons = weapons
        self.lock_x = 0
        self.weapon_range = 0

        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.lock_x
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (150, 150, 80), 2, 4 * rate])

    def start_(self):
        self.instructor.animate_loop("defeat")
        self.lock_x = self.instructor.c_rect().left + self.instructor.c_rect().width / 2

    def get_distance(self, target):
        self_volume_circle = self.instructor.volume_circle()
        target_volume_circle = target.get_volume_circle()
        return self_volume_circle.distance(target_volume_circle)

    def update_(self):
        if self.lock_target is None:
            now_lock_unit = None
            now_lock_range = 999999
            for i in self.instructor.radar_list():
                if not i.wait_to_death and not i.state_label.contain_flag(["hidden", "invincible"]) \
                        and self.weapons.unit_filter(i):
                    distance = self.get_distance(i)
                    weapon = self.weapons.weapon_choose_intellect(i, distance)
                    true_range = distance - weapon.aim_range
                    if distance < now_lock_range and true_range <= 0:
                        now_lock_range = distance
                        now_lock_unit = i

            if now_lock_unit is not None:
                self.lock_target = now_lock_unit
                self.instructions["attack"].target = now_lock_unit
                self.change_now_instruction(self.instructions["attack"])
        else:
            if self.instructions["attack"].end is True:
                self.lock_target = None
                self.change_now_instruction(None)
                return

    def clear(self):
        super().clear()
        self.weapons = None
        self.lock_target = None
