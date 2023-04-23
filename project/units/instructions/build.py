from unit_tools.instruction import Instruction
from auxiliary_tools.message_manager import MessageManager
from units.effect.create_special_effect import CreateSpecialEffect
from math import floor


class Build(Instruction):
    def __init__(self, skill, build_x, left, build_time, building_name, height_c, width):
        super().__init__(skill)
        self.build_x = build_x
        self.is_building = False
        self.building = None
        self.left = left
        self.build_frame = int(build_time * 60)
        self.total_frame = int(build_time * 60)
        self.frame_rate = 0.95 / self.build_frame
        self.building_frame = 0

        special_effect = CreateSpecialEffect(effect_name=building_name, path="./data/img/units/building/",
                                             size=(width, 0), auto_clear=False, index=-1, blend_color=(200, 200, 150))
        building_point = left + width / 2
        self.building_shadow = special_effect.take_effect((building_point, 800 - height_c), None)

        self.draw_time = 1

    def draw(self):
        self.draw_time += 1 if self.draw_time < 21 else -20
        rate = self.draw_time / 20
        center = self.build_x
        MessageManager.send_message("ellipse_draw", [center, 20 * rate, (60, 255, 60), 2, 4 * rate])

    def start_(self):
        self.instructor.add_label("no_pushing")

    def update(self):
        if self.building is not None and self.building.wait_to_death:
            self.end = True
            return

        self.instructor.animate_speed(self.instructor.attribute("speed_rate"))
        self.instructor.animate_loop("walk")
        if not self.is_building and self.instructor.approach(self.build_x, 30):
            if not self.skill.check_buildable(self.build_x):
                self.end = True
                return
            effect = self.skill.take_effect()
            if effect is not None:
                if self.building_shadow is not None:
                    self.building_shadow.clear()
                    self.building_shadow = None

                self.is_building = True
                self.removable = False
                self.instructor.add_label("uncontrollable")
                self.instructor.add_label("hidden")
                self.instructor.panel_change()
                self.instructor.set_visible(False)
                self.building = effect.take_effect((self.left, 0), self.skill.unit)
                self.building.start_build()
                hm_bar = self.building.behavior_manager.get("HMBar")
                if hm_bar is not None:
                    hm_bar.chant_bar_color = 100, 155, 255
            else:
                self.end = True
                return
        elif self.is_building:
            self.build_frame -= 1
            self.building.attribute_manager.health_recovery(
                self.frame_rate * self.building.attribute_manager.get_attribute("max_health"))
            hm_bar = self.building.behavior_manager.get("HMBar")
            chant_rate = 1 - self.build_frame / self.total_frame
            if hm_bar is not None:
                hm_bar.chant_bar = chant_rate
            build_length = self.building.atlas.atlas_dict.get("build")
            build_frame = floor(len(build_length) * chant_rate * 0.99) if build_length is not None else None
            if build_frame is not None and build_frame != self.building_frame:
                self.building_frame = build_frame
                self.building.animate_controler.set_animate_frame("build", build_frame)
            if self.build_frame <= 0:
                self.building.finish_build()
                self.end = True
                self.if_finish = True
                return

    def clear(self):
        if self.building_shadow is not None:
            self.building_shadow.clear()
            self.building_shadow = None
        if self.instructor is not None:
            if self.building is not None:
                hm_bar = self.building.behavior_manager.get("HMBar")
            else:
                hm_bar = None
            if hm_bar is not None:
                hm_bar.chant_bar = 0
                hm_bar.chant_bar_color = 200, 200, 200
            self.instructor.remove_label("no_pushing")
            self.instructor.remove_label("uncontrollable")
            self.instructor.remove_label("hidden")
            self.instructor.panel_change()
            self.instructor.set_visible(True)
        self.building = None
        super().clear()
