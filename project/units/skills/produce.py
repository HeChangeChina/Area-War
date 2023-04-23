from unit_tools.skill import Skill
from units.effect.create_unit import CreateUnit
from units.instructions.produce import Produce
from auxiliary_tools.resources_manager import ResourcesManager


class ProduceSkill(Skill):
    def __init__(self, unit, produce_unit_name, unit_icon, cost, population_cost, time_requirement=10,
                 tech_require=None, tech_mode="have", animate=None, flag="None"):
        effect = CreateUnit(unit_name=produce_unit_name)
        self.time_requirement = time_requirement / 5
        self.animate = animate
        super().__init__(unit, None, effect=effect, tech_require=tech_require, tech_mode=tech_mode, quick_spell=False)
        self.flag.add_flag(["produce", "instruction_replace"])
        self.flag.add_flag(flag)

        self.produce_instruction = self.unit.attribute_manager.get_attribute("produce_instruction")
        if self.produce_instruction is None:
            self.produce_instruction = Produce(animate)
            self.unit.instructor.add_instruction(self.produce_instruction)

        self.produce_unit_icon = unit_icon
        self.cost = cost
        self.population_cost = population_cost

        self.resource_cost_show = cost
        self.resource_cost_show["population"] = population_cost

    def start_recall(self):
        return True

    def finish_recall(self):
        ResourcesManager.add_resources("population", value=-self.population_cost, team=self.unit.team)
        x = self.unit.c_rect.left + self.unit.c_rect.width / 2
        y = self.unit.c_rect.top + self.unit.c_rect.height / 2
        self.effect.take_effect((x, y), self.unit)

    def cancel_recall(self):
        for i in self.cost:
            if i != "population":
                ResourcesManager.add_resources(i, self.cost[i], self.unit.team)
        ResourcesManager.add_resources("population", value=-self.population_cost, team=self.unit.team)

    def get_instruction(self, data):
        for i in self.cost:
            if i != "population":
                ResourcesManager.add_resources(i, -self.cost[i], self.unit.team)
        ResourcesManager.add_resources("population", value=self.population_cost, team=self.unit.team)
        self.produce_instruction.add_production(self.produce_unit_icon, self.time_requirement, self.finish_recall
                                                , self.cancel_recall, self.start_recall)
        return None

    def data_check(self, data):
        for i in self.cost:
            if ResourcesManager.get_resources(i, self.unit.team) < self.cost[i] and i != "population":
                return False
        if ResourcesManager.get_resources("max_population", self.unit.team) - \
                ResourcesManager.get_resources("population", self.unit.team) < self.population_cost:
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

