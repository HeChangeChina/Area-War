from unit_tools.skill import Skill


class NullSkill(Skill):
    def __init__(self):
        super().__init__(None, None)

    def before_take_effect_check(self):
        return True

    def before_use_check(self):
        return True
