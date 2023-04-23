from units.units import Unit
from auxiliary_tools.building_gird import BuildingGird
from auxiliary_tools.resources_manager import ResourcesManager
from units.ground import Ground
from units.skills.attack import SkillAttack
from units.skills.stop import SkillStop
from units.skills.cancel_build import SkillCancelBuild
from units.skills.set_rally_point import SetRallyPoint
from console.skill_panel import SkillPanel


class Building(Unit):
    def __init__(self, atlas, unit_name, c_rect, attribute_manager, unit_height=280, unit_height_c=0,
                 weapons=None, gird_layer=0, team=0, volume=15, radar_range=400, population_cost=0, population_produce=0):
        super().__init__(atlas, unit_name, c_rect, attribute_manager, unit_height, unit_height_c, weapons,
                         team, volume, radar_range, population_cost, population_produce)
        self.flag.add_flag(["building", "land_force", "repairable"])
        self.layer = -3 + gird_layer

        self.height_controller.change_mode(1)
        self.height_controller.update()
        self.c_rect.top = self.height_controller.target_height + unit_height_c

        self.animate_controler.lock_side = True

        skill_attack = SkillAttack(self)
        skill_stop = SkillStop(self)
        skill_set_point = SetRallyPoint(self)
        skill_cancel_build = SkillCancelBuild(self)
        skill_remove = SkillCancelBuild(self, 0.3, 0.9)
        self.skill_manager.add(skill_set_point)
        self.skill_manager.add(skill_attack)
        self.skill_manager.add(skill_stop)
        self.skill_manager.add(skill_cancel_build)
        self.skill_manager.add(skill_remove)

        self.skill_panel.replace("SkillStop", skill_stop, describe="停止&停止单位当前的指令",
                                 key="S", line=0, column=2, mouse=False)
        self.skill_panel.replace("SkillAttack", skill_attack, describe="攻击&攻击指定目标或向目标位置周围的敌人",
                                 key="A", line=0, column=1, mouse=True)
        self.skill_panel.replace("SkillSetRP", skill_set_point, describe="设置集结点&生产的单位会前往集结点",
                                 key="G", line=0, column=0, mouse=True)
        self.skill_panel.replace("SkillCancel", skill_remove, describe="拆除&拆除该建筑，返还30%的消耗(需要生命值大于90%%)",
                                 key=None, line=0, column=4, mouse=False)

        left_gird = (Ground.length / 2 + self.c_rect.left) // 50
        self.gird_list = list()
        for i in range(self.c_rect.width // 51 + 1):
            self.gird_list.append(int(left_gird + i))
        BuildingGird.set_gird(self.gird_list, gird_layer)
        self.order = 1

        self.skill_panel_save = None
        self.exp_produce = 10

        self.unit_panel["armor_icon"] = ("wallP", "wallM")

    def base_update(self, data):
        super().base_update(data)

    def finish_build(self):
        self.animate_controler.stop = False
        self.weapons.set_enabled(True)
        self.skill_panel = self.skill_panel_save
        self.skill_panel.panel_change = True
        self.state_label.remove_flag("under_building")
        ResourcesManager.add_resources("max_population", self.population_produce, self.team)

    def start_build(self):
        self.animate_controler.stop = True
        if self.atlas.atlas_dict.get("build") is not None:
            self.animate_controler.set_animate_frame("build", 0)

        ResourcesManager.add_resources("max_population", -self.population_produce, self.team)

        self.weapons.set_enabled(False)

        self.skill_panel_save = SkillPanel()
        self.skill_panel_save.panel = self.skill_panel.panel
        self.skill_panel = SkillPanel()

        skill_set_point = self.skill_manager.get(["skill", "move"])
        skill_cancel = self.skill_manager.get(["skill", "cancel_build"])
        self.state_label.add_flag("under_building")
        self.skill_panel.replace("SkillSetRP", skill_set_point, describe="设置集结点&生产的单位会前往集结点",
                                 key="G", line=0, column=1, mouse=True)
        self.skill_panel.replace("SkillCancel", skill_cancel, describe="取消&取消建造，返还75%的消耗",
                                 key="T", line=0, column=0, mouse=True)

        self.attribute_manager.health = self.attribute_manager.get_attribute("max_health") / 20

    def clear(self):
        BuildingGird.remove_gird(self.gird_list, self.layer + 3)
        super().clear()
