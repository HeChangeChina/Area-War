from unit_tools.instruction import Instruction
from auxiliary_tools.resources_manager import ResourcesManager
from auxiliary_tools.message_manager import MessageManager


class Collect(Instruction):
    def __init__(self, skill, animate, collect_speed, target=None, storehouse=None):
        super().__init__(skill)
        self.animate = animate
        self.target = target
        self.storehouse = storehouse
        self.collect_speed = collect_speed / 60

        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        if self.target is not None:
            draw_x = self.target.c_rect.left + self.target.c_rect.width / 2
            MessageManager.send_message("ellipse_draw", [draw_x, 15 * rate, (255, 255, 255), 2, 4 * rate])
        elif self.storehouse is not None:
            draw_x = self.storehouse.c_rect.left + self.storehouse.c_rect.width / 2
            MessageManager.send_message("ellipse_draw", [draw_x, 15 * rate, (255, 255, 255), 2, 4 * rate])

    def change_target(self):
        if self.target is not None and self.instructor.unit in self.target.collect_unit:
            self.target.collect_unit.remove(self.instructor.unit)
            self.target.collect_vacancy += 1

    def start_(self):
        if self.target is not None and self.target.collect_vacancy <= 0:
            self.target = self.search_new_resource(self.target.resource_type)
            if self.target is None and self.now_carry_resource() == 0:
                self.end = True
            elif self.target is None:
                self.storehouse = self.search_storehouse()
                if self.storehouse is None:
                    self.end = True

    def distance(self, target):
        return abs(self.instructor.c_rect().left + self.instructor.c_rect().width / 2 - target.c_rect.left - target.c_rect.width / 2)

    def search_storehouse(self):
        distance = 9999
        target = None
        for i in self.instructor.radar_list():
            now_distance = self.distance(i)
            if i.flag.contain_flag("storehouse") and i.team == self.instructor.team() and now_distance < distance:
                target = i
                distance = now_distance
        return target

    def now_carry_resource(self):
        return self.instructor.unit.attribute_manager.get_attribute("resource_carry")[1]

    def now_carry_type(self):
        return self.instructor.unit.attribute_manager.get_attribute("resource_carry")[0]

    def set_carry(self, carry_type, value):
        self.instructor.unit.attribute_manager.set_attribute("resource_carry", [carry_type, value])

    def add_carry(self, value):
        self.instructor.unit.attribute_manager.set_attribute("resource_carry",
                                                             [self.now_carry_type(), self.now_carry_resource() + value])

    def get_limit(self):
        return self.instructor.unit.attribute_manager.get_attribute("resource_carry_limit")

    def search_new_resource(self, resource_type):
        for i in self.instructor.radar_list():
            if i.flag.contain_flag("resource") and i.resource_type == resource_type and i.collect_vacancy > 0 and\
                    i.revising is False:
                return i
        return None

    def update_(self):
        if self.target is None and self.storehouse is None:
            self.end = True
            return

        if self.target is not None:
            center_x = self.target.c_rect.left + self.target.c_rect.width / 2
            approach_range = self.target.volume
            if self.instructor.approach(center_x, approach_range) or \
                    self.instructor.in_distance(center_x, approach_range * 1.3):
                if self.instructor.unit not in self.target.collect_unit:
                    if self.target.collect_vacancy > 0:
                        self.target.collect_unit.append(self.instructor.unit)
                        self.target.collect_vacancy -= 1
                    elif self.target.collect_vacancy <= 0:
                        self.change_target()
                        self.target = self.search_new_resource(self.target.resource_type)
                        if self.target is None:
                            self.storehouse = self.search_storehouse()
                            if self.storehouse is None:
                                self.end = True
                        return

                self.instructor.animate_speed(1)
                self.instructor.animate_loop(self.animate)
                if self.now_carry_type() != self.target.resource_type:
                    self.set_carry(self.target.resource_type, 0)

                if self.target.revising:
                    self.change_target()
                    self.target = None
                    self.storehouse = self.search_storehouse()
                    if self.storehouse is None:
                        self.end = True
                    return

                if self.target.resource_stock > self.collect_speed:
                    self.instructor.remove_label("no_pushing")
                    self.add_carry(self.collect_speed)
                    self.target.resource_stock -= self.collect_speed
                    if self.now_carry_resource() > self.get_limit():
                        self.target.resource_stock += self.now_carry_resource() - self.get_limit()
                        self.set_carry(self.target.resource_type, self.get_limit())
                        self.change_target()
                        self.target = None
                        self.storehouse = self.search_storehouse()
                        if self.storehouse is None:
                            self.end = True
                            return
                else:
                    self.change_target()
                    self.target = self.search_new_resource(self.target.resource_type)
                    if self.target is None:
                        self.storehouse = self.search_storehouse()
                        if self.storehouse is None:
                            self.end = True
                            return
            else:
                self.instructor.add_label("no_pushing")
                self.instructor.animate_loop("walk")
                self.instructor.animate_speed(self.instructor.attribute("speed_rate"))

        elif self.storehouse is not None:
            center_x = self.storehouse.c_rect.left + self.storehouse.c_rect.width / 2
            approach_range = self.storehouse.volume
            if self.instructor.approach(center_x, approach_range):
                ResourcesManager.add_resources(self.now_carry_type(), self.now_carry_resource() * 5,
                                               self.instructor.unit.team)
                self.set_carry(self.now_carry_type(), 0)
                self.storehouse = None
                self.target = self.search_new_resource(self.now_carry_type())
                if self.target is None:
                    self.end = True
                    return
            else:
                self.instructor.add_label("no_pushing")
                self.instructor.animate_loop("walk")
                self.instructor.animate_speed(self.instructor.attribute("speed_rate"))

    def clear(self):
        if self.instructor is not None:
            self.instructor.remove_label("no_pushing")
            self.instructor.animate_speed(1)
        self.change_target()
        self.target = None
        self.storehouse = None
        super().clear()
