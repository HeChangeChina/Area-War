from base import Base


class AttributeRevise(Base):
    def __init__(self):
        super().__init__()
        self.if_clear = False
        self.revise_list = []
        self.level = 1
        self.attribute_list = list()

    def set_attribute_list(self, attr_list):
        self.attribute_list = attr_list
        for i in self.revise_list:
            if i[0] not in self.attribute_list:
                self.revise_list.remove(i)

    def add(self, attribute, value, flag):
        if attribute in self.attribute_list:
            self.revise_list.append([attribute, value, flag])
        else:
            print("Waring: not acceptable revise type:" + str(attribute))

    def set(self, flag, value):
        for i in range(len(self.revise_list)):
            if self.revise_list[i][2] == flag:
                self.revise_list[i][1] = value
                break

    def get(self, flag):
        for i in range(len(self.revise_list)):
            if self.revise_list[i][2] == flag:
                return self.revise_list[i]

    def remove(self, flag):
        for i in range(len(self.revise_list)):
            if self.revise_list[i][2] == flag:
                del self.revise_list[i]
                break

    def attribute_update(self, attribute_dict):
        for i in self.revise_list:
            if i[0] == "max_health":
                attribute_dict["max_health"] += i[1] * self.level
            elif i[0] == "max_magic":
                attribute_dict["max_magic"] += i[1] * self.level
            elif i[0] == "health_recovery_rate":
                attribute_dict["health_recovery_rate"] += i[1] * self.level
            elif i[0] == "magic_recovery_rate":
                attribute_dict["magic_recovery_rate"] += i[1] * self.level
            elif i[0] == "health_recovery_speed":
                attribute_dict["health_recovery_speed"] += i[1] * self.level
            elif i[0] == "magic_recovery_speed":
                attribute_dict["magic_recovery_speed"] += i[1] * self.level
            elif i[0] == "weight":
                attribute_dict["weight"] += i[1] * self.level
            elif i[0] == "speed":
                attribute_dict["speed"] += i[1] * self.level
            elif i[0] == "speed_rate":
                attribute_dict["speed_rate"] += i[1] * self.level
            elif i[0] == "physical_armor":
                attribute_dict["physical_armor"] += i[1] * self.level
            elif i[0] == "magic_armor":
                attribute_dict["magic_armor"] += i[1] * self.level
            elif i[0] == "hurt_rate":
                attribute_dict["hurt_rate"] += i[1] * self.level
            elif i[0] == "weapon_speed":
                attribute_dict["weapon_speed"] += i[1] * self.level
            elif i[0] == "harm_cause_rate":
                attribute_dict["harm_cause_rate"] += i[1] * self.level
        return attribute_dict

    def clear(self):
        super().clear()
        self.if_clear = True
