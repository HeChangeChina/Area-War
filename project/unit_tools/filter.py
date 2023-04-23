from base import Base
from auxiliary_tools.flag_manager import FlagManager
from unit_tools.team_manager import TeamManager


class NullFilter(Base):
    def __init__(self, point=False):
        super().__init__()
        self.point = point

    def filter(self, f_object):
        if self.point is False:
            return False
        elif type(f_object) is tuple or type(f_object) is list:
            return True
        else:
            return False


class Filter(Base):
    def __init__(self, unit, required_flag=None, excluded_flag=None, included_flag=None, point=False):
        super().__init__()
        self.required_flag = list(required_flag) if required_flag is not None else list()
        self.excluded_flag = list(excluded_flag) if excluded_flag is not None else list()
        self.included_flag = list(included_flag) if included_flag is not None else list()
        self.unit = unit
        self.point = point

    def filter(self, f_object):
        if type(f_object) is list or type(f_object) is tuple:
            return self.point
        else:
            flag = FlagManager()
            flag.add_flag(f_object.flag.flag)
            if f_object.team == self.unit.team:
                flag.add_flag("own")
            elif TeamManager.is_alliance(self.unit.team, f_object.team):
                flag.add_flag("ally")
            else:
                flag.add_flag("enemy")
            if f_object == self.unit:
                flag.add_flag("self")

            require = flag.contain_flag(self.required_flag, must_have_all=True)
            excluded = f_object.flag.contain_flag(self.excluded_flag) is False if len(self.excluded_flag) > 0 else True
            included = flag.contain_flag(self.included_flag)
            return require and excluded and included

    def clear(self):
        super().clear()
        self.unit = None


class FilterUnion(Base):
    def __init__(self):
        super().__init__()
        self.filters = list()
        self.point = True

    def add(self, filter_object):
        self.filters.append(filter_object)

    def remove(self, filter_object):
        self.filters.remove(filter_object)

    def filter(self, f_object):
        if type(f_object) is tuple or type(f_object) is list and self.point:
            return True
        for i in self.filters:
            if i.filter(f_object):
                return True
        return False
