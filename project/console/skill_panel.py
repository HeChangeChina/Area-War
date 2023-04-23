from base import Base


class SkillPanel(Base):
    def __init__(self):
        super().__init__()
        self.panel = {"defeat": list()}
        for i in range(20):
            self.panel["defeat"].append((None, None, None, None, None, None))
        self.panel_change = False

    def replace(self, button_icon, skill, key=None, mouse=False, describe="技能", panel_to=None, line=0, column=0,
                panel="defeat"):
        if self.panel.get(panel) is None:
            self.panel[panel] = []
            for i in range(20):
                self.panel[panel].append((None, None, None, None, None, None))
        self.panel[panel][line * 5 + column] = (button_icon, skill, key, mouse, describe, panel_to)
        self.panel_change = True

    def get(self, line, column, panel="defeat"):
        return self.panel[panel][line + column * 4]

    def get_panel(self, panel="defeat"):
        if self.panel.get(panel) is not None:
            return self.panel[panel]
        else:
            return_panel = list()
            for i in range(20):
                return_panel.append((None, None, None, None, None, None))
            return return_panel

    def clear(self):
        super().clear()
        self.panel.clear()
