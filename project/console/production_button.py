from base import Base
from console.production_bar import ProductionBar
from console.unit_production_button import UnitProductionButton
from unit_tools.team_manager import TeamManager


class ProductionButton(Base):
    def __init__(self, x, y):
        super().__init__()
        self.unit = None
        self.first_draw = False
        self.bar = ProductionBar(x + 55, y + 13)
        self.button_list = list()
        self.under_control = True
        for i in range(7):
            if i == 0:
                button = UnitProductionButton(x, y, None, self, i)
            else:
                button = UnitProductionButton(x + (i - 1) * 55, y + 55, None, self, i)
            self.button_list.append(button)

    def set_unit(self, unit):
        self.unit = unit
        if unit is not None:
            self.first_draw = False
            self.under_control = TeamManager.is_player(unit.team) and unit.state_label.contain_flag("uncontrollable") is False
            for i in self.button_list:
                i.controllable = self.under_control

    def button_down(self, index):
        self.unit.attribute_manager.get_attribute("produce_instruction").cancel_production(index)

    def update(self):
        if self.unit is not None:
            self.bar.update()
            for i in self.button_list:
                i.update()

            production_list = self.unit.attribute_manager.get_attribute("production_list")
            production_list_change = self.unit.attribute_manager.get_attribute("production_list_change")
            if production_list_change or self.first_draw is False:
                self.first_draw = True
                self.unit.attribute_manager.set_attribute("production_list_change", False)
                for i in range(len(production_list)):
                    self.button_list[i].change_unit(production_list[i])

            production_bar = self.unit.attribute_manager.get_attribute("production_bar")
            if production_bar is not None:
                self.bar.change_rate(production_bar[0], production_bar[1])

    def move_to(self, x, y):
        self.bar.move_to(x + 55, y + 13)
        for i in range(7):
            if i == 0:
                self.button_list[i].move_to(x, y)
            else:
                self.button_list[i].move_to(x + (i - 1) * 55, y + 55)

    def get_surface(self):
        surface_list = list()
        if self.unit is not None:
            for i in self.bar.get_surface():
                surface_list.append(i)
            for i1 in self.button_list:
                for i2 in i1.get_surface():
                    surface_list.append(i2)

        return surface_list

    def clear(self):
        self.unit = None
        self.bar.clear()
        for i in self.button_list:
            i.clear()
        self.bar = None
        self.button_list = list()
        super().clear()
