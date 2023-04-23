from base import Base


class SkillManager(Base):
    def __init__(self):
        super().__init__()
        self.skill_list = []

    def add(self, skill):
        if type(skill) is list:
            for i in skill:
                self.skill_list.append(i)
        else:
            self.skill_list.append(skill)

    def remove(self, skill):
        for i in self.skill_list:
            if i.flag.contain_flag(skill, must_have_all=True):
                self.skill_list.remove(i)
                break

    def get(self, skill_flag):
        for i in self.skill_list:
            if i.flag.contain_flag(skill_flag, must_have_all=True):
                return i
        return None

    def get_by_obj(self, skill):
        for i in self.skill_list:
            if i == skill:
                return i
        return None

    def filter_target(self, data, skill_limit=None):
        if skill_limit is None:
            skill_list = self.skill_list
        else:
            skill_list = list()
            for i in self.skill_list:
                for i2 in skill_limit:
                    if i.flag.contain_flag(i2, must_have_all=True):
                        skill_list.append(i)
        for i in skill_list:
            if i.target_mode is not None and i.target_mode.filter(data):
                return i
        return None

    def update(self):
        for i in self.skill_list:
            i.update()
            if i.if_auto_use:
                data = i.auto_use()
                if data is not False:
                    i.unit.controller.use_skill(i.flag.flag, data[0], data[1])

    def get_instruction_by_flag(self, flag, data, have_indicator=True):
        for i in self.skill_list:
            if i.flag.contain_flag(flag, must_have_all=True):
                i.have_indicator = have_indicator
                return i.get_instruction(data)
        return None

    def clear(self):
        super().clear()
        for i in self.skill_list:
            i.clear()
        self.skill_list = []
