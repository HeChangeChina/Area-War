from unit_tools.instruction import Instruction
from units.skills.null_skill import NullSkill


class Produce(Instruction):
    def __init__(self, produce_animate=None):
        super().__init__(NullSkill())
        self.additional = True
        self.production_list = list()
        self.now_time = 0
        self.if_producing = False
        self.exp_defeat = None
        self.base_info_defeat = None
        self.produce_animate = produce_animate

    def start_(self):
        self.instructor.unit.attribute_manager.create_attribute("produce_instruction", self)
        self.instructor.unit.attribute_manager.create_attribute("production_list", [None, None, None, None, None, None, None])
        self.instructor.unit.attribute_manager.create_attribute("production_list_change", True)
        self.instructor.unit.attribute_manager.create_attribute("production_bar", [0, 10])

    def add_production(self, unit_icon, time, finish_recall=None, cancel_recall=None, start_recall=None):
        if len(self.production_list) < 7:
            self.production_list.append((unit_icon, time, finish_recall, cancel_recall, start_recall))
            if len(self.production_list) == 1:
                self.now_time = time * 60
            self.set_attr_list()

    def cancel_production(self, index):
        self.production_list[index][3]()
        self.production_list.pop(index)
        if index == 0 and len(self.production_list) > 0:
            self.now_time = self.production_list[0][1] * 60
        self.now_time += 1
        self.set_attr_list()
        self.update_()

    def set_attr_list(self):
        attr_list = list()
        for i in self.production_list:
            attr_list.append(i[0])
        while len(attr_list) < 7:
            attr_list.append(None)
        self.instructor.unit.attribute_manager.set_attribute("production_list", attr_list)
        self.instructor.unit.attribute_manager.set_attribute("production_list_change", True)

    def update_(self):
        if self.produce_animate is not None:
            defeat_action = "produce" if self.if_producing else "defeat"
            self.instructor.animate_loop(defeat_action)

        if len(self.production_list) > 0 and self.if_producing is False:
            self.if_producing = True
            self.base_info_defeat = self.instructor.get_panel("base_info")
            self.exp_defeat = self.instructor.get_panel("exp_info")
            self.instructor.set_panel("base_info", None)
            self.instructor.set_panel("exp_info", None)
            self.instructor.set_panel("production_info", 25)
        elif len(self.production_list) == 0 and self.if_producing:
            self.if_producing = False
            self.instructor.set_panel("base_info", self.base_info_defeat)
            self.instructor.set_panel("exp_info", self.exp_defeat)
            self.instructor.set_panel("production_info", None)

        if len(self.production_list) > 0:
            if self.now_time <= 0:
                self.production_list[0][2]()
                self.production_list.pop(0)
                if len(self.production_list) > 0:
                    if self.production_list[0][4]():
                        self.now_time = self.production_list[0][1] * 60
                    else:
                        while len(self.production_list) > 0 and self.production_list[0][4]() is False:
                            self.production_list[0][3]()
                            self.production_list.pop(0)
                        if len(self.production_list) > 0:
                            self.now_time = self.production_list[0][1] * 60
                self.set_attr_list()
                self.update_()
            else:
                self.now_time -= 1
                rate = 1 - self.now_time / (self.production_list[0][1] * 60)
                self.instructor.unit.attribute_manager.set_attribute("production_bar",
                                                                     [rate, self.production_list[0][1]])

    def clear(self):
        if self.instructor.unit is not None:
            self.instructor.unit.attribute_manager.delete_attribute("produce_instruction")
            self.instructor.unit.attribute_manager.delete_attribute("production_list")
            self.instructor.unit.attribute_manager.delete_attribute("production_list_change")
            self.instructor.unit.attribute_manager.delete_attribute("production_bar")

        for i in self.production_list:
            i[3]()
        self.production_list = list()
        super().clear()
