from auxiliary_tools.tech_tree import TechTree
from unit_tools.skill import Skill


class LearnSkill(Skill):
    def __init__(self, unit, hero_level_tech, skill_point_require, skill_point_tech, upgrade_tech, hero_level_require=0,
                 skill_point_base=0, flag="learn"):
        super().__init__(unit, None)
        self.flag.add_flag(flag)
        self.hero_level_tech = hero_level_tech
        self.hero_level_require = hero_level_require
        self.skill_point_require = skill_point_require
        self.skill_point_tech = skill_point_tech
        self.upgrade_tech = upgrade_tech
        self.skill_point_base = skill_point_base

        self.enabled = not TechTree.have_tech(self.unit.team, upgrade_tech)

    def get_instruction(self, data):
        self.update()
        if self.enabled:
            TechTree.set_level(self.upgrade_tech, self.unit.team)
            TechTree.add_level(self.skill_point_tech, self.unit.team, self.skill_point_require)

    def update(self):
        super().update()
        skill_point_cost = TechTree.get_level(self.unit.team, self.skill_point_tech)
        hero_level = TechTree.get_level(self.unit.team, self.hero_level_tech)
        skill_point_have = hero_level - skill_point_cost + self.skill_point_base
        self.enabled = skill_point_have >= self.skill_point_require and hero_level >= self.hero_level_require and not\
            TechTree.have_tech(self.unit.team, self.upgrade_tech)

