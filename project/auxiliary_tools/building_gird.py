class BuildingGird:
    gird = list()
    @classmethod
    def reset_gird(cls, length):
        cls.gird = list()
        for i1 in range(3):
            now_gird = list()
            for i2 in range(length):
                now_gird.append(False)
            cls.gird.append(now_gird)

    @classmethod
    def check_gird(cls, gird_list, gird_layer=0):
        for i in gird_list:
            if cls.gird[gird_layer][i]:
                return False
        return True

    @classmethod
    def remove_gird(cls, gird_list, gird_layer=0):
        for i in gird_list:
            cls.gird[gird_layer][i] = False

    @classmethod
    def set_gird(cls, gird_list, gird_layer=0):
        for i in gird_list:
            cls.gird[gird_layer][i] = True
