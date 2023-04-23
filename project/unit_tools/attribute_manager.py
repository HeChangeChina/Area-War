from base import Base
from unit_tools.attribute_revise_manager import AttributeReviseManager
from unit_tools.behavior_manager import BehaviorManager
from auxiliary_tools.tech_tree import TechTree
import copy


class AttributeManager(Base):
    def __init__(self, team=0, max_health=100, max_magic=10, health_recovery_speed=0.4, magic_recovery_speed=0.4, weight=10,
                 speed=0.8, physical_armor=1, magic_armor=10, armor_level_add=(1, 5), armor_tech=("", ""), health=-1,
                 magic=-1, exp_tech=None, exp_amount_tech=None, exp_tech_team_change=False):
        super().__init__()
        self.base_attribute_dict = {"max_health": max_health, "max_magic": max_magic,
                                    "health_recovery_speed": health_recovery_speed,
                                    "magic_recovery_speed": magic_recovery_speed, "weight": weight, "speed": speed,
                                    "health_recovery_rate": 1, "magic_recovery_rate": 1, "speed_rate": 1,
                                    "hurt_rate": 1, "physical_armor": physical_armor, "magic_armor": magic_armor,
                                    "weapon_speed": 1, "harm_cause_rate": 1}
        self.attribute_dict = {"max_health": max_health, "max_magic": max_magic,
                               "health_recovery_speed": health_recovery_speed,
                               "magic_recovery_speed": magic_recovery_speed, "weight": weight, "speed": speed,
                               "health_recovery_rate": 1, "magic_recovery_rate": 1, "speed_rate": 1,
                               "hurt_rate": 1, "physical_armor": physical_armor, "magic_armor": magic_armor,
                               "weapon_speed": 1, "harm_cause_rate": 1}
        if health > 0:
            self.health = health
        else:
            self.health = max_health
        if magic > 0:
            self.magic = magic
        else:
            self.magic = max_magic

        self.level = 1
        self.exp = 0
        self.exp_level = [100]
        self.hm_level_up = [(25, 10)]
        self.exp_tech = exp_tech
        self.exp_amount_tech = exp_amount_tech
        self.exp_team_change = exp_tech_team_change
        self.team = team
        self.armor_tech = armor_tech

        self.base_armor = (physical_armor, magic_armor)
        self.armor_level = [0, 0]
        self.armor_level_add = armor_level_add
        self.armor_tech = armor_tech
        self.armor_level[0] = TechTree.get_level(armor_tech[0], team)
        self.armor_level[1] = TechTree.get_level(armor_tech[1], team)
        if self.armor_tech[0] == self.armor_tech[1]:
            self.message_require("tech_" + armor_tech[0] + "_change", self.armor_change)
        else:
            self.message_require("tech_" + armor_tech[0] + "_change", self.armor_change)
            self.message_require("tech_" + armor_tech[1] + "_change", self.armor_change)

        self.behavior_manager = BehaviorManager(self)
        self.attribute_revise_manager = AttributeReviseManager()
        self.attribute_revise_manager.set_attribute_list(self.base_attribute_dict)

    def change_team(self, team):
        self.team = team
        self.armor_level[0] = TechTree.get_level(team, self.armor_tech[0])
        self.armor_level[1] = TechTree.get_level(team, self.armor_tech[1])
        armor = self.base_armor[0] + self.armor_level_add[0] * self.armor_level[0]
        self.base_attribute_dict["physical_armor"] = armor
        armor = self.base_armor[1] + self.armor_level_add[1] * self.armor_level[1]
        self.base_attribute_dict["magic_armor"] = armor

        if self.exp_team_change:
            self.level = TechTree.get_level(team, self.exp_tech) if self.exp_tech is not None else self.level
            if self.level == 0:
                self.level += 1
            self.exp = TechTree.get_level(team, self.exp_amount_tech) if self.exp_amount_tech is not None else self.exp
            self.add_exp(0)

    def get_now_exp_level(self):
        return self.exp_level[self.level - 1]

    def add_exp(self, exp):
        self.exp += exp
        while self.exp >= self.exp_level[self.level - 1]:
            if len(self.exp_level) > self.level:
                self.exp -= self.exp_level[self.level - 1]
                self.base_attribute_dict["max_health"] += self.hm_level_up[self.level - 1][0]
                self.base_attribute_dict["max_magic"] += self.hm_level_up[self.level - 1][1]
                self.health += self.hm_level_up[self.level - 1][0]
                self.magic += self.hm_level_up[self.level - 1][1]
                self.level += 1
                if self.exp_tech is not None:
                    TechTree.set_level(self.exp_tech, self.team, self.level)
            else:
                self.exp = self.exp_level[self.level - 1]
                break
        if self.exp_amount_tech is not None:
            TechTree.set_level(self.exp_amount_tech, self.team, self.exp)

    def create_attribute(self, attribute, value):
        self.base_attribute_dict[attribute] = value
        self.attribute_dict[attribute] = value
        self.attribute_revise_manager.set_attribute_list(self.base_attribute_dict)

    def add_attribute(self, attribute, value):
        if self.base_attribute_dict is not None:
            self.base_attribute_dict[attribute] += value

    def set_attribute(self, attribute, value):
        if self.base_attribute_dict is not None:
            self.base_attribute_dict[attribute] = value

    def delete_attribute(self, attribute):
        if self.base_attribute_dict is not None:
            self.base_attribute_dict.pop(attribute)
            self.attribute_dict.pop(attribute)
            self.attribute_revise_manager.set_attribute_list(self.base_attribute_dict)

    def get_attribute(self, attribute):
        if self.attribute_dict is not None:
            return self.attribute_dict.get(attribute)
        else:
            return None

    def armor_change(self, data):
        if data[2] == self.team:
            if data[0] == self.armor_tech[0]:
                self.armor_level[0] = data[1]
                armor = self.base_armor[0] + self.armor_level_add[0] * self.armor_level[0]
                self.base_attribute_dict["physical_armor"] = armor
            if data[0] == self.armor_tech[1]:
                self.armor_level[1] = data[1]
                armor = self.base_armor[1] + self.armor_level_add[1] * self.armor_level[1]
                self.base_attribute_dict["magic_armor"] = armor

    def hurt(self, value, hurt_type, have_event=True):
        hurt = value
        if hurt_type == 0:
            hurt = value - self.attribute_dict["physical_armor"]
            if hurt < value * 0.1:
                hurt = value * 0.1
            hurt *= self.attribute_dict["hurt_rate"]
            self.health -= hurt
        elif hurt_type == 1:
            hurt = value * ((100 - self.attribute_dict["magic_armor"]) / 100)
            hurt *= self.attribute_dict["hurt_rate"]
            self.health -= hurt
        else:
            hurt *= self.attribute_dict["hurt_rate"]
            self.health -= hurt
        if have_event:
            self.behavior_manager.hurt(hurt, hurt_type)

    def magic_use(self, value, have_event=True):
        if self.magic > value:
            self.magic -= value
        else:
            value = self.magic
            self.magic = 0
        if have_event:
            self.behavior_manager.magic_use(value)

    def health_recovery(self, value, recovery_type=0, have_event=True):
        recovery = value * self.attribute_dict["health_recovery_rate"]
        self.health += recovery if recovery_type == 0 else value
        if self.health >= self.attribute_dict["max_health"]:
            self.health = self.attribute_dict["max_health"]
        if have_event:
            self.behavior_manager.health_recovery(recovery)

    def magic_recovery(self, value, recovery_type=0, have_event=True):
        recovery = value * self.attribute_dict["magic_recovery_rate"]
        self.magic += recovery if recovery_type == 0 else value
        if self.magic >= self.attribute_dict["max_magic"]:
            self.magic = self.attribute_dict["max_magic"]
        if have_event:
            self.behavior_manager.magic_recovery(recovery)

    def get_speed(self):
        return self.attribute_dict["speed"] * self.attribute_dict["speed_rate"]

    def get_weight(self):
        return self.attribute_dict["weight"]

    def update(self):
        if self.attribute_dict is not None:
            self.attribute_dict = self.attribute_revise_manager.attribute_update(copy.copy(self.base_attribute_dict))
            if self.attribute_dict["health_recovery_rate"] < 0:
                self.attribute_dict["health_recovery_rate"] = 0
            if self.attribute_dict["magic_recovery_rate"] < 0:
                self.attribute_dict["magic_recovery_rate"] = 0
            if self.attribute_dict["speed_rate"] < 0.2:
                self.attribute_dict["speed_rate"] = 0.2
            if self.attribute_dict["health_recovery_speed"] < 0:
                self.attribute_dict["health_recovery_speed"] = 0
            if self.attribute_dict["magic_recovery_speed"] < 0:
                self.attribute_dict["magic_recovery_speed"] = 0
            if self.attribute_dict["speed"] < 0:
                self.attribute_dict["speed"] = 0
            if self.attribute_dict["weight"] < 0:
                self.attribute_dict["weight"] = 0
            if self.attribute_dict["magic_armor"] > 90:
                self.attribute_dict["magic_armor"] = 90
            if self.attribute_dict["hurt_rate"] < 0:
                self.attribute_dict["hurt_rate"] = 0
            if self.attribute_dict["weapon_speed"] < 0.1:
                self.attribute_dict["weapon_speed"] = 0.1
            if self.health > self.attribute_dict["max_health"]:
                self.health = self.attribute_dict["max_health"]
            if self.magic > self.attribute_dict["max_magic"]:
                self.magic = self.attribute_dict["max_magic"]
            self.health_recovery(self.attribute_dict["health_recovery_speed"] / 60, have_event=False)
            self.magic_recovery(self.attribute_dict["magic_recovery_speed"] / 60, have_event=False)

    def clear(self):
        super().clear()
        self.attribute_dict = None
        self.base_attribute_dict = None
        self.attribute_revise_manager.clear()
        self.behavior_manager = None
