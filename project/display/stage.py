import pygame
from base import Base
from display.shader import Shader
from units.sight.building import BuildingSight


class Stage(Base):
    def __init__(self, left, top, width, height, father_surface, draw_on_father=False):
        super().__init__()
        self.show_list = []
        self.rect = pygame.Rect(left, top, width, height)
        self.clear_rect = []
        self.father_surface = father_surface
        self.draw_on_father = draw_on_father
        if draw_on_father is True:
            self.surface = father_surface
        else:
            self.surface = pygame.Surface((width, height)).convert_alpha()
        self.blend_color = (0, 0, 0)
        self.sky_box = (100, 80, 80)
        self.shader = Shader()
        self.shader.set_surface(self.surface)
        self.camera_shifting = [0, 0]
        self.camera_limit = [[-1000, 1000], [-1000, 1000]]

        self.mouse_on = None
        self.mouse_down = False
        self.mouse_down_obj_ = None
        self.mouse_up = False

        self.start_update()

    def move_camera(self, shifting):
        self.camera_shifting[0] += shifting[0]
        self.camera_shifting[1] += shifting[1]

        if self.camera_shifting[0] < self.camera_limit[0][0]:
            self.camera_shifting[0] = self.camera_limit[0][0]
        elif self.camera_shifting[0] > self.camera_limit[0][1]:
            self.camera_shifting[0] = self.camera_limit[0][1]

        if self.camera_shifting[1] < self.camera_limit[1][0]:
            self.camera_shifting[1] = self.camera_limit[1][0]
        elif self.camera_shifting[1] > self.camera_limit[1][1]:
            self.camera_shifting[1] = self.camera_limit[1][1]

    def set_camera(self, camera):
        self.camera_shifting = camera

        if self.camera_shifting[0] < self.camera_limit[0][0]:
            self.camera_shifting[0] = self.camera_limit[0][0]
        elif self.camera_shifting[0] > self.camera_limit[0][1]:
            self.camera_shifting[0] = self.camera_limit[0][1]

        if self.camera_shifting[1] < self.camera_limit[1][0]:
            self.camera_shifting[1] = self.camera_limit[1][0]
        elif self.camera_shifting[1] > self.camera_limit[1][1]:
            self.camera_shifting[1] = self.camera_limit[1][1]

    def set_camera_limit_x(self, left, right):
        limit = [left, right]
        self.camera_limit[0] = limit

    def set_camera_limit_y(self, top, bottom):
        limit = [top, bottom]
        self.camera_limit[1] = limit

    def set_sky_box(self, color):
        self.sky_box = color

    def add(self, display_object, index=0, z=1):
        self.show_list.append([display_object, index, z])
        self.sort()

    def sort(self):
        self.show_list = sorted(self.show_list, key=(lambda x: [x[1], x[0].c_rect.left + x[0].c_rect.width / 2]))

    def lift(self, display_object, index=0):
        for i in range(len(self.show_list)):
            if self.show_list[i][0] == display_object:
                self.show_list[i][1] = index
                break

    def remove(self, display_object):
        for i in range(len(self.show_list)):
            if self.show_list[i][0] == display_object:
                # print("object:" + str(self.show_list[i]) + " have been remove form stage, now left " + str(
                #     len(self.show_list) - 1))
                del self.show_list[i]
                break

    def draw(self, draw_list, z):
        surface = draw_list[0]
        rect = self.get_rel_rect(draw_list[1], z)
        if -rect.width < rect.left < 1920 and -rect.height < rect.top < 1080:
            self.surface.blit(surface, rect)
            return True
        return False

    def get_rel_rect(self, rect, z):
        return pygame.Rect(rect.left + self.camera_shifting[0] * z,
                           rect.top + self.camera_shifting[1] * z,
                           rect.width, rect.height)

    def stop_update(self):
        self.message_remove("update_60")

    def start_update(self):
        self.message_require("update_60", self.graph_update)
        self.message_require("stop_update_60", self.graph_update)

    def update(self):
        pass

    def before_draw(self):
        pass

    def surface_rendering(self, surface_list, object_list):
        return surface_list

    def mouse_click(self, target, mouse):
        pass

    def mouse_down_obj(self, target, mouse):
        pass

    def mouse_down_pos(self, mouse):
        pass

    def mouse_up_obj(self, target, mouse):
        pass

    def mouse_up_pos(self, mouse):
        pass

    def mouse_enter(self, target, mouse):
        pass

    def mouse_leave(self, target, mouse):
        pass

    def mouse_event_update(self):
        mouse_c = pygame.mouse.get_pos()
        mouse_surface = pygame.Surface((1, 1))
        mouse_mask = pygame.mask.from_surface(mouse_surface)
        mouse_on = None

        mouse_down = pygame.mouse.get_pressed(3)[0]
        if_mouse_down = False
        if_mouse_up = False
        if mouse_down is True and self.mouse_down is False:
            if_mouse_down = True
        elif mouse_down is False and self.mouse_down is True:
            if_mouse_up = True
        self.mouse_down = mouse_down

        for i in self.show_list[::-1]:
            if i[0].mouse_enabled is True and i[0].in_screen and i[0].visible:
                surface_list = i[0].get_surface()[0]
                mask = pygame.mask.from_surface(surface_list[0])
                surface_rect = self.get_rel_rect(surface_list[1], i[2])
                c_list = [- surface_rect.left + mouse_c[0], - surface_rect.top + mouse_c[1]]
                point = mask.overlap(mouse_mask, c_list)
                if point is not None:
                    mouse_on = i[0]
                    break

        if mouse_on != self.mouse_on:
            if self.mouse_on is not None:
                self.mouse_on.mouse_out()
                self.mouse_leave(self.mouse_on, mouse_c)
            if mouse_on is not None:
                mouse_on.mouse_in()
                self.mouse_enter(mouse_on, mouse_c)
            self.mouse_on = mouse_on
        if if_mouse_up and self.mouse_on is not None and self.mouse_on == self.mouse_down_obj_:
            self.mouse_on.mouse_click()
            self.mouse_click(self.mouse_on, mouse_c)
        if if_mouse_down and self.mouse_on is not None:
            self.mouse_on.mouse_down()
            self.mouse_down_obj(self.mouse_on, mouse_c)
            self.mouse_down_obj_ = self.mouse_on
        if if_mouse_up and self.mouse_on is not None:
            self.mouse_on.mouse_up()
            self.mouse_up_obj(self.mouse_on, mouse_c)
        if if_mouse_down:
            self.mouse_down_pos(mouse_c)
        if if_mouse_up:
            self.mouse_down_obj_ = None
            self.mouse_up_pos(mouse_c)

    def graph_update(self, data):
        self.mouse_event_update()
        self.sort()
        self.before_draw()
        if self.sky_box[0] > 0:
            if len(self.clear_rect) > 0:
                for i in self.clear_rect:
                    pass
                    self.surface.fill(self.sky_box, i)
            else:
                pass
                self.surface.fill(self.sky_box)

        delete_list = []
        for i in self.show_list:
            if i[0].if_clear is False:
                if i[0].visible is True:
                    surface_list = i[0].get_surface()
                    if len(surface_list) > 0:
                        surface_list[0] = self.surface_rendering(surface_list[0], i)
                    in_screen = False
                    for i2 in surface_list:
                        in_screen = self.draw(i2, z=i[2])
                    i[0].in_screen = in_screen
            else:
                delete_list.append(i[0])
        for i in delete_list:
            self.remove(i)
        if self.blend_color != (0, 0, 0):
            self.surface.fill(self.blend_color, rect=self.rect, special_flags=pygame.BLEND_MULT)
        if self.draw_on_father is False:
            self.father_surface.blit(self.surface, self.rect)
        if data != "stop":
            self.update()
