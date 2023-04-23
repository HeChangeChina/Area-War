from console.console_button import ConsoleButton


class BehaviorButton(ConsoleButton):
    def __init__(self, c_xy, behavior):
        self.behavior = behavior
        self.total_frame = behavior.last_frame
        icon = self.behavior.icon
        text = self.behavior.name + "&" + self.behavior.describe
        if self.behavior.polarity == "positive":
            frame = "BehaviorFramePositive"
        elif self.behavior.polarity == "negative":
            frame = "BehaviorFrameNegative"
        else:
            frame = "BehaviorFrameDefeat"
        super().__init__(c_xy, img=icon, text=text, frame=frame, size=(30, 30))

    def update(self):
        super().update()
        if self.behavior is not None:
            if 0 < self.behavior.last_frame < 240 and self.total_frame > 480:
                rate = 1 - (self.behavior.last_frame % 30 + 30) / 60 if self.behavior.last_frame % 60 <= 30 else \
                    (self.behavior.last_frame % 30 + 30) / 60
                self.surface.set_alpha((rate * 255))
            elif self.behavior.last_frame == 0:
                self.behavior = None
