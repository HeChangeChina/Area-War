from base import Base


class BehaviorManager(Base):
    def __init__(self, attribute_manager):
        super().__init__()
        self.attribute_manager = attribute_manager
        self.unit = None
        self.behavior_list = []

    def set_unit(self, unit):
        self.unit = unit

    def add(self, behavior):
        for i in self.behavior_list:
            if i.flag.contain_flag(behavior.flag.flag, must_have_all=True):
                i.add_level()
                return
        behavior.set_manager(self)
        self.behavior_list.append(behavior)

    def get(self, flag):
        for i in self.behavior_list:
            if i.flag.contain_flag(flag):
                return i

    def clear_behaviors(self):
        for i in self.behavior_list:
            i.clear()
        self.behavior_list = list()

    def remove(self, behavior):
        behavior.clear()
        self.behavior_list.remove(behavior)

    def remove_from_flag(self, flag, must_have_all=True):
        have_flag = []
        for i in self.behavior_list:
            if i.flag.contain_flag(flag, must_have_all=must_have_all):
                have_flag.append(i)
        for i in have_flag:
            self.remove(i)

    def hurt(self, value, hurt_type):
        for i in self.behavior_list:
            i.hurt(value, hurt_type)

    def magic_use(self, value):
        for i in self.behavior_list:
            i.magic_use(value)

    def health_recovery(self, value):
        for i in self.behavior_list:
            i.health_recovery(value)

    def magic_recovery(self, value):
        for i in self.behavior_list:
            i.magic_recovery(value)

    def clear(self):
        super().clear()
        self.remove_from_flag("behavior")
        self.attribute_manager = None
        self.unit = None

    def update_15(self):
        for i in self.behavior_list:
            i.update_15()

    def update_60(self):
        for i in self.behavior_list:
            i.base_update_60()
