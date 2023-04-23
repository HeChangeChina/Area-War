from unit_tools.effect import Effect


class Hurt(Effect):
    def effect(self, target, trigger):
        if self.data.get("have_event") is None:
            self.data["have_event"] = True
        if self.data.get("value") is None or self.data.get("hurt_type") is None:
            print("Warning: effect 'hurt' got the wrong data, 'value' or 'hurt_type' is missing.")
            return
        if self.data["have_event"]:
            target.shader.flash()
        hurt_value = self.data["value"] * trigger.attribute_manager.get_attribute("harm_cause_rate")
        if target.wait_to_death is False:
            target.attribute_manager.hurt(hurt_value, self.data["hurt_type"], self.data["have_event"])
            target.controller.hurt(trigger)
            if target.attribute_manager.health <= 0:
                target.death(trigger)
