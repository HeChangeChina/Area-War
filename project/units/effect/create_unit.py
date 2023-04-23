from unit_tools.effect import Effect
from auxiliary_tools.message_manager import MessageManager
from auxiliary_tools.unit_factory import UnitFactory


class CreateUnit(Effect):
    def take_effect(self, target, trigger):
        if self.data.get("unit_name") is None:
            print("Warning: effect 'CreateUnit' got the wrong data, 'unit' is missing.")
            return
        if self.data.get("team") is None:
            self.data["team"] = trigger.team

        unit = UnitFactory.produce(self.data["unit_name"], target[0], target[1])
        if unit is None:
            print("Warning: effect 'CreateUnit' can't find '" + self.data["unit_name"] + "' in unit factory.")
            return 
        unit.change_team(self.data["team"])
        MessageManager.send_message("create_unit", unit)
        rally_point = trigger.attribute_manager.get_attribute("RallyPoint")
        if rally_point is not None:
            if type(rally_point) is not float and type(rally_point) is not int:
                rally_point = rally_point.c_rect.left + rally_point.c_rect.width / 2
            unit.controller.use_skill(["skill", "attack"], (rally_point, 0), have_indicator=False)
        return unit
