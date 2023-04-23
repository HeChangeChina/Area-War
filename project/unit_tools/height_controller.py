from base import Base


class HeightController(Base):
    def __init__(self, height, target_height, mode=0):
        super().__init__()
        self.height = height
        self.target_height = target_height
        self.mode = mode
        self.cal_fun = None
        if mode == 0:
            self.cal_fun = self.calculate_mode_0
        elif mode == 1:
            self.cal_fun = self.calculate_mode_1
        elif mode == 2:
            self.cal_fun = self.calculate_mode_2
        self.speed = 0

    def change_mode(self, mode):
        self.mode = mode
        if mode == 0:
            self.cal_fun = self.calculate_mode_0
        elif mode == 1:
            self.cal_fun = self.calculate_mode_1
        elif mode == 2:
            self.cal_fun = self.calculate_mode_2

    def calculate_mode_1(self):
        self.height = self.target_height

    def calculate_mode_0(self):
        # print(str(self.height)+"..."+str(self.target_height))
        if self.height < self.target_height:
            self.height = self.target_height
            self.speed = 0
        else:
            if self.height - self.target_height < 5:
                self.height = self.target_height
                self.speed = 0
            else:
                self.speed += 30 / 60
                self.height -= self.speed
                if self.height < self.target_height:
                    self.height = self.target_height
                    self.speed = 0

    def calculate_mode_2(self):
        # print(str(self.height)+"..."+str(self.target_height))
        if abs(self.height - self.target_height) < 5:
            self.height = self.target_height
        elif self.height > self.target_height:
            self.height -= 3
        elif self.height < self.target_height:
            self.height += 3

    def update(self):
        self.cal_fun()
