from console.console_button import ConsoleButton


class WeaponShower(ConsoleButton):
    def __init__(self, weapon, c_xy):
        super().__init__(c_xy)
        self.weapon = weapon
        self.level = self.weapon.level
        self.enabled = self.weapon.enabled
        if self.enabled:
            name = self.weapon.name + "&等级:"
        else:
            name = self.weapon.name + "(已禁用)&等级:"
        text = name + str(self.weapon.level) + "&" + self.weapon.hurt_describe + ":" + str(
            self.weapon.hurt) + "&范围:" + str(
            self.weapon.aim_range) + "&基础间隔:" + str(self.weapon.interval) + "s&" + self.weapon.describe
        self.change(img=self.weapon.icon, corner=str(self.weapon.level))
        self.change_text(text)

    def update(self):
        if self.level != self.weapon.level or self.enabled != self.weapon.enabled:
            self.level = self.weapon.level
            self.enabled = self.weapon.enabled
            if self.enabled:
                name = self.weapon.name + "&等级:"
            else:
                name = self.weapon.name + "(已禁用)&等级:"
            text = name + str(self.weapon.level) + "&" + self.weapon.hurt_describe + ":" + str(
                self.weapon.hurt) + "&范围:" + str(
                self.weapon.aim_range) + "&" + self.weapon.describe
            self.change(img=self.weapon.icon, corner=str(self.weapon.level))
            self.change_text(text)
        super().update()

    def clear(self):
        super().clear()
        self.weapon = None
