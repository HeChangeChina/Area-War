from console.console_button import ConsoleButton
from auxiliary_tools.message_manager import MessageManager


class FormationButton(ConsoleButton):
    def __init__(self, c_xy, corner):
        self.corner = str(corner)
        if corner == 1:
            self.chosen = True
            img = "FormationBGC"
            frame = "FormationFrameC"
        else:
            self.chosen = False
            img = "FormationBG"
            frame = "FormationFrame"
        super().__init__(c_xy, size=(40, 20), corner=str(corner), frame=frame, img_source="./data/img/console", img=img)
        self.message_require("FormationChoose", self.change_chosen)

    def change_chosen(self, corner):
        corner = str(corner)
        self.chosen = self.corner == corner

        if self.chosen:
            img = "FormationBGC"
            frame = "FormationFrameC"
        else:
            img = "FormationBG"
            frame = "FormationFrame"

        self.change(img_source="./data/img/console", img=img, frame=frame, corner=str(self.corner))

    def mouse_down(self):
        MessageManager.send_message("FormationChoose", self.corner)
