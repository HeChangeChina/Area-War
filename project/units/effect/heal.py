from unit_tools.effect import Effect


class Heal(Effect):
    def effect(self, target, trigger):
        if self.data.get("have_event") is None:
            self.data["have_event"] = True
            if self.data.get("heal_type") is None:
                self.data["heal_type"] = 0
        if self.data.get("value") is None:
            print("Warning: effect 'hurt' got the wrong data, 'value' or 'hurt_type' is missing.")
            return
        if target.wait_to_death is False:
            target.attribute_manager.health_recovery(self.data["value"], self.data["heal_type"], self.data["have_event"])
