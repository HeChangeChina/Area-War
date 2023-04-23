from units.units import Unit
from units.skills.move import SkillMove
from units.skills.stop import SkillStop
from units.skills.attack import SkillAttack
from units.skills.hold import SkillHold
from units.skills.patrol import SkillPatrol


class MovableUnit(Unit):
    def __init__(self, atlas, unit_name, c_rect, attribute_manager, unit_height=280, unit_height_c=0,
                 weapons=None, team=0, volume=15, radar_range=400, population_cost=0, population_produce=0):
        super().__init__(atlas, unit_name, c_rect, attribute_manager, unit_height, unit_height_c, weapons,
                         team, volume, radar_range, population_cost, population_produce)
        self.flag.add_flag("movable_unit")
        self.pushing_active_time = 15

        move_skill = SkillMove(self)
        stop_skill = SkillStop(self)
        attack_skill = SkillAttack(self)
        hold_skill = SkillHold(self)
        patrol_skill = SkillPatrol(self)
        self.skill_manager.add(move_skill)
        self.skill_manager.add(stop_skill)
        self.skill_manager.add(attack_skill)
        self.skill_manager.add(hold_skill)
        self.skill_manager.add(patrol_skill)

        self.skill_panel.replace("SkillMove", move_skill, describe="移动&移动至指定位置",
                                 key="D", line=0, column=0, mouse=True)
        self.skill_panel.replace("SkillStop", stop_skill, describe="停止&停止单位当前的指令",
                                 key="S", line=0, column=1, mouse=False)
        self.skill_panel.replace("SkillAttack", attack_skill, describe="攻击/进军&攻击指定目标或向目标位置进军",
                                 key="A", line=0, column=2, mouse=True)
        self.skill_panel.replace("SkillHold", hold_skill, describe="保持不动&原地保持不动，仅攻击武器范围内的敌人",
                                 key="H", line=0, column=3, mouse=False)
        self.skill_panel.replace("SkillPatrol", patrol_skill, describe="巡逻&在当前位置与目标位置间巡逻，攻击发现的敌人",
                                 key="P", line=0, column=4, mouse=False)

    def push(self, force):
        c_x = 2 / self.attribute_manager.attribute_dict["weight"] * force
        self.c_rect.left += c_x
        if abs(c_x) > 0.5:
            self.pushing_active_time = 15

    def update_15(self):
        if self.pushing_active_time > 0:
            self.pushing_active_time -= 1
        if self.state_label.contain_flag("no_pushing") is False and self.pushing_active_time > 0:
            for i in self.radar_list:
                if (i.state_label.contain_flag("no_pushing") or i.wait_to_death) or \
                        i.flag.contain_flag("movable_unit") is False:
                    continue
                distance = self.get_radar().center_distance(i.get_radar())
                if distance < self.volume:
                    if self.c_rect.left + self.c_rect.width / 2 > i.c_rect.left + i.c_rect.width / 2:
                        i.push(-self.attribute_manager.attribute_dict["weight"] * (2 - 1 * distance / self.volume))
                    else:
                        i.push(self.attribute_manager.attribute_dict["weight"] * (2 - 1 * distance / self.volume))

    def update_60(self):
        self.update_60_m()

    def update_60_m(self):
        pass
