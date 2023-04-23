from unit_tools.effect import Effect
from auxiliary_tools.tech_tree import TechTree


class MixedEffect(Effect):
    def take_effect(self, target, trigger):
        if self.data.get("effects") is None:
            print("Warning: effect 'CreateSpecialEffect' got the wrong data, 'effect_name' is missing.")
            return

        for i in self.data["effects"]:
            if type(i) is not tuple:
                i.take_effect(target, trigger)
            elif TechTree.have_tech(trigger.team, i[1]):
                i[0].take_effect(target, trigger)
