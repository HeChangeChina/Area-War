from unit_tools.skill import Skill
from unit_tools.effect import Effect
from units.instructions.produce import Produce
from auxiliary_tools.resources_manager import ResourcesManager
from auxiliary_tools.tech_tree import TechTree


class ResearchSkill(Skill):
    def __init__(self, unit, cost, research_icon, effect=None, tech=None, time_requirement=10,
                 tech_require=None, tech_mode="have", animate=None, flag="None", auto_use=False,
                 idle_use=False):
        effect = Effect() if effect is None else effect
        self.tech = tech
        self.time_requirement = time_requirement / 5
        self.animate = animate
        self.idle_use = idle_use
        super().__init__(unit, None, effect=effect, tech_require=tech_require, tech_mode=tech_mode, quick_spell=False,
                         can_auto_use=auto_use)
        self.flag.add_flag(["research", "instruction_replace"])
        self.flag.add_flag(flag)

        self.produce_instruction = self.unit.attribute_manager.get_attribute("produce_instruction")
        if self.produce_instruction is None:
            self.produce_instruction = Produce(animate)
            self.unit.instructor.add_instruction(self.produce_instruction)

        self.research_icon_icon = research_icon
        self.cost = cost

        self.resource_cost_show = cost

    def start_recall(self):
        self.update()
        return self.enabled

    def auto_use_judge(self):
        if self.idle_use and self.unit.state_label.contain_flag("under_building") is False:
            produce_list = self.unit.attribute_manager.get_attribute("production_list")
            if produce_list is not None and produce_list[0] is None:
                return None, "None"
            else:
                return False
        else:
            return False

    def finish_recall(self):
        x = self.unit.c_rect.left + self.unit.c_rect.width / 2
        y = self.unit.c_rect.top + self.unit.c_rect.height / 2
        self.effect.take_effect(self.unit, self.unit)

        if self.tech is not None:
            TechTree.add_level(self.tech, self.unit.team)

    def cancel_recall(self):
        for i in self.cost:
            ResourcesManager.add_resources(i, self.cost[i], self.unit.team)

    def get_instruction(self, data):
        for i in self.cost:
            ResourcesManager.add_resources(i, -self.cost[i], self.unit.team)
        self.produce_instruction.add_production(self.research_icon_icon, self.time_requirement, self.finish_recall
                                                , self.cancel_recall, self.start_recall)
        return None

    def data_check(self, data):
        for i in self.cost:
            if ResourcesManager.get_resources(i, self.unit.team) < self.cost[i]:
                return False
        return True

    def update(self):
        super().update()
        produce_list = self.unit.attribute_manager.get_attribute("production_list")
        if produce_list is not None:
            count = 0
            while produce_list[count] is not None:
                count += 1
                if count == 7:
                    break
            self.instruction_count = count

