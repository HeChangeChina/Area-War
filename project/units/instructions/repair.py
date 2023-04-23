from unit_tools.instruction import Instruction
from auxiliary_tools.resources_manager import ResourcesManager
from auxiliary_tools.message_manager import MessageManager
from copy import copy


class Repair(Instruction):
    def __init__(self, skill, target, animate="skill", repair_speed=15):
        super().__init__(skill)
        self.target = target
        self.animate = animate
        self.approach = False
        self.repair_speed = repair_speed / 60
        self.cost_cycle = 0

        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.target.c_rect.left + self.target.c_rect.width / 2
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (60, 255, 60), 2, 4 * rate])

    def update(self):
        if self.target.state_label.contain_flag("hidden") or self.target.wait_to_death:
            self.end = True
            return

        target_x = self.target.c_rect.left + self.target.c_rect.width / 2
        if self.instructor.in_distance(target_x, self.target.volume * 1.2) and self.approach:
            self.instructor.remove_label("no_pushing")
            cost = copy(self.target.cost)
            for i in cost:
                cost[i] *= self.repair_speed * 30 / self.target.attribute_manager.get_attribute("max_health")
            for i in cost:
                if ResourcesManager.get_resources(i, self.instructor.team()) < cost[i]:
                    self.end = True
                    return
            self.instructor.animate_loop(self.animate)
            self.target.attribute_manager.health_recovery(self.repair_speed, 1)
            self.cost_cycle -= 1 if self.cost_cycle > 0 else 0
            if self.cost_cycle == 0:
                self.cost_cycle = 30
                for i in cost:
                    ResourcesManager.add_resources(i, -cost[i], self.instructor.team())

            if self.target.attribute_manager.health >= self.target.attribute_manager.get_attribute("max_health"):
                self.end = True
                self.if_finish = True
                return
        else:
            self.instructor.animate_loop("walk")
            self.instructor.add_label("no_pushing")
            self.approach = self.instructor.approach(target_x, self.target.volume * 0.9)

    def clear(self):
        self.target = None
        self.instructor.remove_label("no_pushing")
        super().clear()
