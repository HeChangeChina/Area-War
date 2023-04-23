from unit_tools.skill import Skill
from unit_tools.filter import NullFilter
from units.sight.building import BuildingSight
from units.ground import Ground
from units.effect.create_unit import CreateUnit
from units.instructions.build import Build
from auxiliary_tools.building_gird import BuildingGird
from auxiliary_tools.resources_manager import ResourcesManager


class BuildSkill(Skill):
    def __init__(self, unit, building_name, height_c, width, gird_layer, cost, build_time=10, tech_require=None,
                 tech_mode=None):
        sight = BuildingSight(building_name, height_c, width, gird_layer)
        effect = CreateUnit(unit_name=building_name)
        super().__init__(unit, NullFilter(True), sight=sight, effect=effect, quick_spell=False,
                         tech_require=tech_require, tech_mode=tech_mode)
        self.flag.add_flag(["build", "instruction_replace"])
        self.flag.add_flag(building_name)
        self.building = building_name
        self.gird_layer = gird_layer
        self.width = width
        self.cost = cost
        self.build_time = build_time / 5
        self.height_c = height_c

        self.gird_list = list()
        self.waiting_start_count = 0
        self.target_x = 0
        self.resource_cost_show = cost

    def cancel(self):
        super().cancel()
        if self.waiting_start_count > 0:
            self.waiting_start_count -= 1
            for i in self.cost:
                ResourcesManager.add_resources(i, self.cost[i], self.unit.team)

    def before_take_effect_check_else(self):
        self.waiting_start_count -= 1
        return True

    def set_target(self, x):
        self.target_x = x

    def get_instruction(self, data):
        self.instruction_count += 1
        for i in self.cost:
            ResourcesManager.add_resources(i, -self.cost[i], self.unit.team)
        left = ((Ground.length / 2 + data[0] - self.width / 2) // 50) * 50 - Ground.length / 2
        return Build(self, data[0], left, self.build_time, self.building, self.height_c, self.width)

    def check_buildable(self, x):
        left_gird = (Ground.length / 2 + x - self.width / 2) // 50
        gird_list = list()
        for i in range(self.width // 51 + 1):
            gird_list.append(int(left_gird + i))
        self.gird_list = gird_list
        return BuildingGird.check_gird(gird_list, self.gird_layer)

    def data_check(self, data):
        x = data[0]
        left_gird = (Ground.length / 2 + x - self.width / 2) // 50
        gird_list = list()
        for i in range(self.width // 51 + 1):
            gird_list.append(int(left_gird + i))
        if BuildingGird.check_gird(gird_list, self.gird_layer) is False:
            return False

        for i in self.cost:
            if ResourcesManager.get_resources(i, self.unit.team) < self.cost[i]:
                return False

        return True
