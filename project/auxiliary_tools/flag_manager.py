class FlagManager:
    def __init__(self):
        super().__init__()
        self.flag = list()

    def add_flag(self, flag):
        if type(flag) is not list:
            if self.flag.count(flag) == 0:
                self.flag.append(flag)
        else:
            for i in flag:
                if self.flag.count(i) == 0:
                    self.flag.append(i)

    def remove_flag(self, flag):
        if type(flag) is not list and flag in self.flag:
            self.flag.remove(flag)
        else:
            for i in flag:
                if i in self.flag:
                    self.flag.remove(i)

    def contain_flag(self, flag, must_have_all=False):
        if type(flag) is not list:
            return flag in self.flag
        else:
            contain_amount = 0
            for i in flag:
                if self.flag.count(i) >= 1:
                    contain_amount += 1
            if must_have_all is False:
                if len(flag) > 0:
                    return contain_amount > 0
                else:
                    return True
            else:
                return contain_amount == len(flag)
