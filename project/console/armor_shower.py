from console.console_button import ConsoleButton


class ArmorShower(ConsoleButton):
    def __init__(self, c_xy, unit=None, armor_type=0):
        super().__init__(c_xy)
        self.unit = None
        self.armor_type = armor_type
        self.set_unit(unit)
        self.armor = 0
        self.armor_level = 0

    def set_unit(self, unit):
        self.unit = unit
        if unit is not None:
            if self.armor_type == 0:
                self.armor = unit.attribute_manager.attribute_dict["physical_armor"]
                self.armor_level = unit.attribute_manager.armor_level[0]
                text = unit.unit_panel["armor_name"][0] + "&等级:" + str(self.armor_level) + "&物理伤害减免:" + str(self.armor)
            else:
                self.armor = unit.attribute_manager.attribute_dict["magic_armor"]
                self.armor_level = unit.attribute_manager.armor_level[1]
                text = unit.unit_panel["armor_name"][1] + "&等级:" + str(self.armor_level) + "&魔法伤害减免:" + str(self.armor) + "%"
            self.change(img=unit.unit_panel["armor_icon"][self.armor_type], corner=str(self.armor_level))
            self.change_text(text)

    def update(self):
        if self.unit is not None:
            if self.unit.wait_to_death is True:
                self.set_unit(None)

            if self.unit is not None:
                if self.armor_type == 0:
                    armor_type = "physical_armor"
                else:
                    armor_type = "magic_armor"
                if self.armor_level != self.unit.attribute_manager.armor_level[self.armor_type] or \
                        self.armor != self.unit.attribute_manager.attribute_dict[armor_type]:
                    self.set_unit(self.unit)
        super().update()

    def clear(self):
        super().clear()
        self.unit = None
