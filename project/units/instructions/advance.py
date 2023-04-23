from units.mixed_instruction import MixedInstruction
from units.instructions.attack import AttackTarget
from units.instructions.attack import HoldAttackTarget
from units.instructions.move import Move
from units.skills.null_skill import NullSkill
from auxiliary_tools.message_manager import MessageManager


class Advance(MixedInstruction):
    def __init__(self, skill, weapons, target):
        super().__init__(skill, attack=AttackTarget(NullSkill(), weapons, None),
                         move=Move(target, NullSkill()))
        self.flag.add_flag("stoppable")
        self.target = target
        self.weapons = weapons
        self.lock_target = None
        self.lock_x = 0
        self.coming_back = False
        self.draw_time = 1
        self.side = 0

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.target
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (150, 80, 80), 2, 4 * rate])

    def start_(self):
        self.lock_x = self.instructor.c_rect().left + self.instructor.c_rect().width / 2
        self.side = 1 if self.lock_x > self.target else 0
        self.change_now_instruction(self.instructions["move"])

    def get_distance(self, target):
        self_volume_circle = self.instructor.volume_circle()
        target_volume_circle = target.get_volume_circle()
        return self_volume_circle.distance(target_volume_circle)

    def get_now_lock_distance(self):
        now_x = self.instructor.c_rect().left + self.instructor.c_rect().width / 2
        return abs(now_x - self.lock_x)

    def lock_unit(self):
        now_lock_unit = None
        now_lock_range = 999999
        for i in self.instructor.radar_list():
            if not i.wait_to_death and not i.state_label.contain_flag(["hidden", "invincible"]) \
                    and self.weapons.unit_filter(i):
                distance = self.get_distance(i)
                weapon = self.weapons.weapon_choose_intellect(i, distance)
                true_range = distance - weapon.aim_range
                if distance < now_lock_range and true_range < 200:
                    now_lock_range = distance
                    now_lock_unit = i

        return now_lock_unit

    def update_(self):
        # 尝试锁定单位
        if self.lock_target is None and not self.coming_back:
            lock_unit = self.lock_unit()
            if lock_unit is not None:
                self.lock_target = lock_unit
                self.instructions["attack"].target = lock_unit
                self.change_now_instruction(self.instructions["attack"])
        elif self.lock_target is not None and not self.coming_back:
            lock_end = False
            if self.instructions["attack"].end:
                lock_end = True
            else:
                distance = self.get_distance(self.lock_target)
                weapon = self.weapons.weapon_choose_intellect(self.lock_target, distance)
                true_range = distance - weapon.aim_range
                now_lock_distance = self.get_now_lock_distance()

                now_x = self.instructor.c_rect().left + self.instructor.c_rect().width / 2
                if self.side == 0 and self.target > now_x > self.lock_x:
                    self.lock_x = now_x
                elif self.side == 1 and self.target < now_x < self.lock_x:
                    self.lock_x = now_x

                if true_range > 0:
                    lock_unit = self.lock_unit()
                    if lock_unit != self.lock_target:
                        lock_end = True
                if true_range > 200:
                    lock_end = True
                elif now_lock_distance > 300:
                    self.coming_back = True
                    lock_end = True
            if lock_end:
                self.lock_target = None
                self.instructor.animate_loop("walk")
                self.change_now_instruction(self.instructions["move"])

        elif self.coming_back:
            if self.get_now_lock_distance() < 150:
                self.coming_back = False

        if self.lock_target is None and self.instructions["move"].end:
            self.end = True
            self.if_finish = True

    def clear(self):
        super().clear()
        self.weapons = None
        self.lock_target = None


class HoldAdvance(MixedInstruction):
    def __init__(self, skill, weapons, target):
        super().__init__(skill, attack=HoldAttackTarget(NullSkill(), weapons, None))
        self.flag.add_flag("stoppable")
        self.target = target
        self.weapons = weapons
        self.lock_target = None
        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.target
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (150, 80, 80), 2, 4 * rate])

    def get_distance(self, target):
        self_volume_circle = self.instructor.volume_circle()
        target_volume_circle = target.get_volume_circle()
        return self_volume_circle.distance(target_volume_circle)

    def update_(self):
        # 尝试锁定单位
        if self.lock_target is None:
            now_lock_unit = None
            now_lock_range = 999999
            for i in self.instructor.radar_list():
                if not i.wait_to_death and not i.state_label.contain_flag(["hidden", "invincible"]) \
                        and self.weapons.unit_filter(i):
                    distance = self.get_distance(i)
                    weapon = self.weapons.weapon_choose_intellect(i, distance)
                    true_range = distance - weapon.aim_range
                    if distance < now_lock_range and true_range < 200:
                        now_lock_range = distance
                        now_lock_unit = i

            if now_lock_unit is not None:
                self.lock_target = now_lock_unit
                self.instructions["attack"].target = now_lock_unit
                self.change_now_instruction(self.instructions["attack"])
            else:
                self.end = True
                return
        else:
            lock_end = self.instructions["attack"].end
            if lock_end:
                self.lock_target = None

    def clear(self):
        super().clear()
        self.weapons = None
        self.lock_target = None
