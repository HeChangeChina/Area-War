from display.display_object import DisplayObject
from unit_tools.team_manager import TeamManager
from pygame import Surface
from pygame import Rect


class Fog(DisplayObject):
    def __init__(self):
        super().__init__()
        self.visible_list = list()
        self.camera_shifting = 0
        self.update_time = 0

    def set_c_shift(self, shift):
        self.camera_shifting = shift

    def in_fog(self, unit):
        for i in self.visible_list:
            if i[1] > self.center_x(unit) > i[0]:
                return False
        return True

    def get_surface(self):
        surface_list = list()
        fog_list = [[0, 1920]]
        for i in self.visible_list:
            remove_list = list()
            for i2 in range(len(fog_list)):
                v_left = i[0] + self.camera_shifting
                v_right = i[1] + self.camera_shifting
                if fog_list[i2][0] < v_left and fog_list[i2][1] > v_right:
                    new_fog001 = [fog_list[i2][0], v_left]
                    new_fog002 = [v_right, fog_list[i2][1]]
                    remove_list.append(fog_list[i2])
                    fog_list.append(new_fog001)
                    fog_list.append(new_fog002)
                elif fog_list[i2][0] > v_left and fog_list[i2][1] < v_right:
                    remove_list.append(fog_list[i2])
                elif fog_list[i2][0] < v_left < fog_list[i2][1]:
                    fog_list[i2][1] = v_left
                elif fog_list[i2][1] > v_right > fog_list[i2][0]:
                    fog_list[i2][0] = v_right
            for i2 in remove_list:
                fog_list.remove(i2)

        for i in fog_list:
            surface = Surface((i[1] - i[0], 810))
            rect = Rect(i[0], 0, i[1] - i[0], 810)
            surface.fill((80, 80, 80))
            surface.set_alpha(200)
            surface_list.append([surface, rect])
        return surface_list

    def fog_update(self, unit_list):
        if self.update_time > 0:
            self.update_time -= 1
            return
        else:
            self.update_time = 4

        player_team = TeamManager.player_team
        visible_list = list()
        for i in unit_list:
            add_fog = True
            if i.team == player_team or TeamManager.is_alliance(player_team, i.team):
                center = self.center_x(i)
                for i2 in range(len(visible_list)):
                    if visible_list[i2][1] > center > visible_list[i2][0]:
                        add_fog = False
                        if center - i.visual_field < visible_list[i2][0]:
                            visible_list[i2][0] = center - i.visual_field
                        if center + i.visual_field > visible_list[i2][1]:
                            visible_list[i2][1] = center + i.visual_field
            else:
                add_fog = False
                center = 0

            if add_fog:
                visible_list.append([center - i.visual_field, center + i.visual_field])

        self.visible_list = visible_list

        for i in unit_list:
            in_fog = self.in_fog(i)
            if in_fog:
                i.visible = False
                i.state_label.add_flag(["in_fog"])
            elif i.state_label.contain_flag(["in_fog"], must_have_all=True):
                i.visible = True
                i.state_label.remove_flag(["in_fog"])

    @staticmethod
    def center_x(unit):
        return unit.c_rect.width / 2 + unit.c_rect.left
