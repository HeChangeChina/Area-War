from base import Base
from unit_tools.filter import FilterUnion
from unit_tools.filter import NullFilter


class WeaponManager(Base):
    def __init__(self, *weapons):
        super().__init__()
        self.weapons = list(weapons)
        self.target_filter = FilterUnion()
        self.if_ready = False
        self.enabled = True

        self.weapon_speed = 1

    def set_enabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self.target_filter_update()
        else:
            self.target_filter = NullFilter()

    def target_filter_update(self):
        if len(self.weapons) > 0:
            self.target_filter = FilterUnion()
            for i in self.weapons:
                self.target_filter.add(i.unit_filter)
            return self.target_filter
        else:
            return NullFilter()

    def add(self, weapon):
        if weapon.mode == "monopolize":
            self.weapons.insert(0, weapon)
        elif weapon.mode == "additional":
            self.weapons.append(weapon)
        self.sort_weapon()
        self.target_filter_update()

    def sort_weapon(self):
        monopolize = list()
        additional = list()
        for i in self.weapons:
            if i.mode == "monopolize":
                monopolize.append(i)
            elif i.mode == "additional":
                additional.append(i)
        monopolize = sorted(monopolize, key=(lambda x: [x.aim_range]), reverse=True)
        additional = sorted(additional, key=(lambda x: [x.aim_range]), reverse=True)
        self.weapons = list()
        for i in monopolize:
            self.weapons.append(i)
        for i in additional:
            self.weapons.append(i)

    def push(self, weapon):
        self.weapons.insert(0, weapon)

    def remove(self, name, describe=None, icon=None):
        for i in self.weapons:
            if i.name == name and (describe is None or i.describe == describe) and (icon is None or i.icon == icon):
                self.weapons.remove(i)
                break
        self.target_filter_update()

    def weapon_choose_conservative(self, target):
        if self.enabled is False:
            return None
        for i in range(len(self.weapons)):
            if self.weapons[i].unit_filter.filter(target):
                return self.weapons[i]

        return None

    def weapon_choose_intellect(self, target, now_range):
        if self.enabled is False:
            return None
        have_monopolize = False
        weapon_choose = self.weapons[0] if self.weapons[0].mode == "monopolize" else None
        for i in range(len(self.weapons)):
            if self.weapons[i].unit_filter.filter(target):
                if self.weapons[i].mode == "monopolize" and now_range < self.weapons[i].aim_range:
                    weapon_choose = self.weapons[i]
                    have_monopolize = True
                elif have_monopolize is False and self.weapons[i].mode == "additional":
                    if self.weapons[i].if_ready:
                        return self.weapons[i]
                    else:
                        continue

        if weapon_choose is not None:
            return weapon_choose

        for i in range(len(self.weapons)):
            if self.weapons[i].unit_filter.filter(target):
                return self.weapons[i]
        return None

    def unit_filter(self, unit):
        if self.enabled is False:
            return False
        for i in self.weapons:
            if i.unit_filter.filter(unit):
                return True
        return False

    def update_ready(self):
        if_ready = False
        for i in self.weapons:
            if i.if_ready:
                if_ready = True
        self.if_ready = if_ready

    def update(self):
        for i in self.weapons:
            i.weapon_speed = self.weapon_speed
            i.update()
        self.update_ready()

    def clear(self):
        super().clear()
        for i in self.weapons:
            i.clear()
        self.weapons = []
