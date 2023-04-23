from unit_tools.instruction import Instruction
from auxiliary_tools.message_manager import MessageManager


class AttackTarget(Instruction):
    def __init__(self, skill, weapons, target):
        super().__init__(skill)
        self.flag.add_flag("attack")
        self.weapons = weapons
        self.target = target
        self.aiming_weapon = None
        self.aiming_time = 0
        self.draw_time = 1
        self.approaching = False

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.target.c_rect.left + self.target.c_rect.width / 2
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (150, 80, 80), 2, 4 * rate])

    def approach_range(self, weapon):
        target_circle = self.target.get_volume_circle()
        return weapon.aim_range + target_circle.radius + self.instructor.volume()

    def now_distance(self):
        self_volume_circle = self.instructor.c_rect().left + self.instructor.c_rect().width / 2
        target_volume_circle = self.target.c_rect.left + self.target.c_rect.width / 2
        return abs(self_volume_circle - target_volume_circle) - self.instructor.volume() - self.target.volume

    def update_(self):
        if self.target.wait_to_death is False and self.target.state_label.contain_flag(["hidden", "invincible"]) is False:
            if self.aiming_weapon is None:
                self.instructor.add_label("no_pushing")
                target_circle = self.target.get_volume_circle()
                target_x = target_circle.center()[0]
                weapon = self.weapons.weapon_choose_intellect(self.target, self.now_distance())
                approach_range = self.approach_range(weapon)
                if self.instructor.approach(target_x, approach_range):
                    self.approaching = False
                    self.instructor.animate_speed(1)
                    self.instructor.animate_loop(weapon.aiming_animate)
                    self.instructor.remove_label("no_pushing")
                    if weapon.if_ready:
                        self.instructor.reset_push()
                        self.aiming_weapon = weapon
                        self.aiming_time = weapon.fire_delay
                        if weapon.fire_animate is not None:
                            self.instructor.animate_play(weapon.fire_animate)
                else:
                    self.approaching = True
                    self.instructor.animate_loop("walk")
                    self.instructor.animate_speed(self.instructor.attribute("speed_rate"))
            if self.aiming_weapon is not None:
                self.instructor.animate_speed(1)
                now_range = self.now_distance()
                if now_range > self.aiming_weapon.escape_range + self.aiming_weapon.aim_range:
                    self.aiming_weapon = None
                    return
                self.aiming_time -= 1
                if self.aiming_time <= 0:
                    effect = self.aiming_weapon.fire()
                    effect.take_effect(self.target, self.instructor.unit)
                    self.aiming_weapon = None
                    return
        else:
            self.end = True

    def clear(self):
        if self.instructor is not None:
            self.instructor.remove_label("no_pushing")
        self.weapons = None
        self.aiming_weapon = None
        super().clear()


class HoldAttackTarget(Instruction):
    def __init__(self, skill, weapons, target):
        super().__init__(skill)
        self.flag.add_flag("attack")
        self.weapons = weapons
        self.target = target
        self.aiming_weapon = None
        self.aiming_time = 0
        self.draw_time = 1
        self.approaching = False

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.target.c_rect.left + self.target.c_rect.width / 2
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (150, 80, 80), 2, 4 * rate])

    def approach_range(self, weapon):
        target_circle = self.target.get_volume_circle()
        return weapon.aim_range + target_circle.radius + self.instructor.volume()

    def now_distance(self):
        self_volume_circle = self.instructor.volume_circle()
        target_volume_circle = self.target.get_volume_circle()
        return self_volume_circle.distance(target_volume_circle)

    def update_(self):
        if self.target.wait_to_death is False and self.target.state_label.contain_flag(["hidden", "invincible"]) is False:
            if self.aiming_weapon is None:
                weapon = self.weapons.weapon_choose_intellect(self.target, self.now_distance())
                approach_range = self.approach_range(weapon)
                if approach_range >= self.now_distance():
                    self.approaching = False
                    self.instructor.animate_speed(1)
                    self.instructor.animate_loop(weapon.aiming_animate)
                    if weapon.if_ready:
                        self.instructor.reset_push()
                        self.aiming_weapon = weapon
                        self.aiming_time = weapon.fire_delay
                        self.instructor.animate_play(weapon.fire_animate)
                else:
                    self.end = True
                    return
            if self.aiming_weapon is not None:
                self.instructor.animate_speed(1)
                now_range = self.now_distance()
                if now_range > self.aiming_weapon.escape_range + self.aiming_weapon.aim_range:
                    self.aiming_weapon = None
                    return
                self.aiming_time -= 1
                if self.aiming_time <= 0:
                    effect = self.aiming_weapon.fire()
                    effect.take_effect(self.target, self.instructor.unit)
                    self.aiming_weapon = None
                    return
        else:
            self.end = True

    def clear(self):
        self.weapons = None
        self.aiming_weapon = None
        super().clear()
