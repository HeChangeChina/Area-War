from units.skills.research import ResearchSkill
from auxiliary_tools.tech_tree import TechTree


class ResearchArmor(ResearchSkill):
    def __init__(self, unit, cost, research_icon, effect=None, tech=None, time_requirement=10,
                 tech_require=None, tech_mode="have", animate=None, flag="None", auto_use=False,
                 idle_use=False, research_level=1):
        super().__init__(unit, cost, research_icon, effect=effect, tech=tech, time_requirement=time_requirement,
                         tech_require=tech_require, tech_mode=tech_mode, animate=animate, flag=flag, auto_use=auto_use,
                         idle_use=idle_use)
        self.research_level = research_level

    def start_recall(self):
        level = TechTree.get_level(self.unit.team, self.tech)
        return level < self.research_level

    def update(self):
        super().update()
        level = TechTree.get_level(self.unit.team, self.tech)
        if level >= self.research_level and self.enabled:
            self.enabled = False
