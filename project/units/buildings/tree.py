from units.building import Building
from units.behaviors.shadow import Shadow
from unit_tools.attribute_manager import AttributeManager
import pygame


class Tree(Building):
    def __init__(self, x, y):
        super().__init__("./data/img/units/buildings/tree", "tree", pygame.Rect(x, y, 100, 160),
                         unit_height_c=165, attribute_manager=AttributeManager(), team=9)
        self.flag.remove_flag("unit")
        self.flag.add_flag(["tree", "resource"])
        self.collect_animate = "shake"
        self.revise_animate = "revise"
        self.resource_stock = 700
        self.resource_limit = 700
        self.resource_type = "wood"
        self.revise_speed = 0.01
        self.collect_vacancy = 2
        self.collect_unit = []
        self.revising = False
        self.volume = 30
        self.cost = dict()

        self.visual_field = 0

        self.behavior_manager.add(Shadow(shadow_size=40))

        self.unit_panel["unit_label"] = ("资源", "树木")
        self.unit_panel["armor_name"] = ("树皮", "树皮")
        self.unit_panel["name"] = "树木"
        self.unit_panel["title"] = "树木"
        self.unit_panel["base_info"] = None
        self.unit_panel["text_y"] = 20
        self.unit_panel["text"] = "资源余量:500/500-再生速度:0.6/秒"

        self.state_label.add_flag(["uncontrollable", "invincible"])

    def update_60(self):
        self.unit_panel["text"] = "资源余量:%.0f/%s-再生速度:%.2f/秒" % (self.resource_stock, self.resource_limit, self.revise_speed * 60)
        self.unit_panel["text"] += "-采集空位:%s" % self.collect_vacancy
        self.resource_stock += self.revise_speed
        if self.collect_vacancy < 2 and self.revising is False:
            self.animate_controler.change_loop_action(self.collect_animate)
        elif self.revising is False:
            self.animate_controler.change_loop_action("defeat")

        if self.resource_stock > self.resource_limit:
            self.resource_stock = self.resource_limit

        if self.resource_stock < 30 and self.revising is False:
            self.revising = True
            self.animate_controler.change_loop_action(self.revise_animate)
            self.state_label.add_flag("revising")
        if self.revising and self.resource_stock > self.resource_limit * 0.2:
            self.revising = False
            self.animate_controler.change_loop_action("defeat")
            self.state_label.remove_flag("revising")

    def clear(self):
        super().clear()
        self.collect_unit = list()

