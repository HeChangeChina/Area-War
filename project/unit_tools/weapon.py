from base import Base
from unit_tools.effect import Effect
from auxiliary_tools.tech_tree import TechTree


class Weapon(Base):
    def __init__(self, unit_filter, team=0, icon="attack", name="武器", describe="一把武器", interval=2.5, effect=None,
                 mode="monopolize", level_up=1, tech="DefeatWeapon", base_hurt=5, hurt_describe="物理伤害:",
                 escape_range=25, aim_range=10, fire_delay=40, fire_animate="attack", aiming_animate="defeat",
                 hurt_effect=None, additional_tech=None, additional_attribute=None):
        super().__init__()
        # 武器模式分为两种，即monopolize(独占),additional(附加),独占模式在拥有目标时不允许其他武器开火，附加模式没有此限制
        self.icon = icon
        self.name = name
        self.describe = describe
        self.interval = interval
        self.effect = effect
        self.mode = mode
        self.escape_range = escape_range
        self.aim_range = aim_range
        self.fire_delay = fire_delay
        self.enabled = True
        self.unit_filter = unit_filter
        self.fire_animate = fire_animate
        self.aiming_animate = aiming_animate
        self.team = team
        self.weapon_speed = 1

        self.tech = tech
        self.level = TechTree.get_level(tech, team)
        self.base_hurt = base_hurt
        self.level_up = level_up
        self.hurt = self.base_hurt + self.level_up * self.level
        self.hurt_describe = hurt_describe
        self.message_require("tech_" + tech + "_change", self.tech_change)

        self.additional_tech = additional_tech
        self.additional_attribute = additional_attribute
        self.additional_have = False

        if self.effect is None:
            self.effect = Effect()

        self.hurt_effect = hurt_effect
        if hurt_effect is not None:
            hurt_effect.data["value"] = self.hurt

        self.if_ready = True
        self.ready_time = 0

    def change_team(self, team):
        self.team = team
        self.level = TechTree.get_level(self.tech, team)
        self.hurt = self.base_hurt + self.level_up * self.level
        if self.hurt_effect is not None:
            self.hurt_effect.data["value"] = self.hurt

    def tech_change(self, data):
        if data[2] == self.team:
            self.level = data[1]
            self.hurt = self.base_hurt + self.level_up * self.level
            if self.hurt_effect is not None:
                self.hurt_effect.data["value"] = self.hurt

    def fire(self):
        self.ready_time = int(self.interval * 60)
        self.if_ready = False
        return self.effect

    def update(self):
        if self.ready_time > 0:
            self.if_ready = False
            self.ready_time -= self.weapon_speed
        elif self.enabled:
            self.if_ready = True
        else:
            self.if_ready = False

        if self.additional_tech is not None and self.additional_have is False:
            if TechTree.have_tech(self.team, self.additional_tech):
                for i in self.additional_attribute:
                    if i == "interval":
                        self.interval += self.additional_attribute[i]
                    elif i == "aim_range":
                        self.aim_range += self.additional_attribute[i]
                self.additional_have = True

    def clear(self):
        super().clear()
        self.unit_filter.clear()
