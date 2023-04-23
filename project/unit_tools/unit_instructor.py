from base import Base


class UnitInstructor(Base):
    def __init__(self, unit):
        super().__init__()
        self.unit = unit
        self.waiting = True
        self.instruction_waiting_list = []
        self.now_instruction = None
        self.additional_instructions = []
        self.enabled = True

    def get_hm_bar(self):
        return self.unit.behavior_manager.get("HMBar")

    def team(self):
        return self.unit.team

    def volume_circle(self):
        return self.unit.get_volume_circle()

    def volume(self):
        return self.unit.volume

    def weapons(self):
        return self.unit.weapons

    def radar(self):
        return self.unit.get_radar()

    def radar_list(self):
        return self.unit.radar_list

    def attribute(self, attr):
        return self.unit.attribute_manager.attribute_dict[attr]

    def c_rect(self):
        return self.unit.c_rect

    def contain_flag(self, flag, must_have_all=False):
        return self.unit.flag.contain_flag(flag, must_have_all)

    def contain_label(self, label, must_have_all=False):
        return self.unit.state_label.contain_flag(label, must_have_all)

    def get_animate_play(self):
        return self.unit.animate_controler.animate_play

    def get_loop_action(self):
        return self.unit.animate_controler.loop_action

    def get_defeat_action(self):
        return self.unit.animate_controler.defeat_action

    def get_speed(self):
        return self.unit.attribute_manager.get_speed()

    def get_panel(self, name):
        return self.unit.unit_panel.get(name)

    def set_panel(self, name, value):
        self.unit.unit_panel[name] = value

    def set_visible(self, visible):
        self.unit.visible = visible

    def face(self, target):
        x = self.c_rect().left + self.c_rect().width / 2
        target = target.c_rect.left + target.c_rect.width / 2
        if x < target:
            self.change_side(0)
        else:
            self.change_side(1)

    def draw_instruction(self):
        if len(self.instruction_waiting_list) > 0 and self.now_instruction is not None:
            self.now_instruction.draw()
            for i in self.instruction_waiting_list:
                i.draw()

    def in_distance(self, target, r=0):
        x = self.c_rect().left + self.c_rect().width / 2
        return abs(target - x) <= r

    def approach(self, target, r=0):
        self.reset_push()
        x = self.c_rect().left + self.c_rect().width / 2
        target = target
        speed = self.get_speed()
        if abs(target - x) <= r:
            if x < target:
                self.change_side(0)
            else:
                self.change_side(1)
            return True
        if x < target:
            self.change_side(0)
            if target - x < speed:
                self.set_x(target)
                return True
            else:
                self.move(speed)
        else:
            self.change_side(1)
            if x - target < speed:
                self.set_x(target)
                return True
            else:
                self.move(-speed)
        return False

    def animate_speed(self, rate):
        self.unit.animate_controler.animate_speed = rate

    def effect(self, effect, target=None, trigger=None):
        if target is None:
            target = self.unit
        if trigger is None:
            trigger = self.unit
        effect.effect(target, trigger)

    def move(self, x):
        self.reset_push()
        self.unit.c_rect.left += x

    def set_x(self, x):
        self.reset_push()
        self.unit.c_rect.left = x - self.c_rect().width / 2

    def reset_push(self):
        if self.contain_flag("movable_unit"):
            self.unit.pushing_active_time = 15

    def add_label(self, label):
        self.unit.state_label.add_flag(label)

    def remove_label(self, label):
        self.unit.state_label.remove_flag(label)

    def animate_play(self, animate):
        self.unit.animate_controler.play_action(animate)

    def animate_loop(self, animate):
        self.unit.animate_controler.change_loop_action(animate)

    def animate_change_defeat_action(self, action):
        self.unit.animate_controler.change_defeat_action(action)

    def animate_return(self):
        self.unit.animate_controler.return_defeat_action()

    def change_side(self, side):
        self.unit.animate_controler.change_side(side)

    def panel_change(self):
        self.unit.skill_panel.panel_change = True

    def insert_instruction(self, instruction):
        if self.now_instruction is not None:
            self.instruction_waiting_list.insert(0, self.now_instruction)
        self.now_instruction = instruction
        instruction.start(self)

    def add_instruction(self, instruction, index=None, clear="clear"):
        if self.enabled:
            if instruction.additional is False:
                self.waiting = False
                if clear == "clear":
                    self.clear_instructions()
                elif clear == "break":
                    self.break_instructions()
                if len(self.instruction_waiting_list) <= 7:
                    if index is None:
                        self.instruction_waiting_list.append(instruction)
                    else:
                        self.instruction_waiting_list.insert(index, instruction)
            else:
                self.additional_instructions.append(instruction)
                instruction.start(self)

    def replace_instruction(self, replace_instruction, new_instruction):
        if self.enabled and replace_instruction is not None:
            if self.now_instruction == replace_instruction and self.now_instruction.removable:
                self.now_instruction.clear()
                self.now_instruction = new_instruction
                new_instruction.start(self)
                return
            for i in range(len(self.instruction_waiting_list)):
                if self.instruction_waiting_list[i] == replace_instruction and self.instruction_waiting_list[i].removable:
                    self.instruction_waiting_list[i].clear()
                    self.instruction_waiting_list[i] = new_instruction
                    return

    def get_instruction(self, skill):
        if self.now_instruction is not None and self.now_instruction.skill == skill:
            return self.now_instruction
        for i in self.instruction_waiting_list:
            if i.skill == skill:
                return i
        return None

    def height_change_mode(self, mode):
        self.unit.height_controller.change_mode(mode)

    def height_target(self, target):
        self.unit.height_controller.target_height = target

    def set_height(self, height):
        self.unit.height_controller.height = height

    def clear_instructions(self):
        for i in self.instruction_waiting_list:
            i.clear()
        self.instruction_waiting_list = []
        if self.now_instruction is not None:
            if self.now_instruction.removable:
                self.now_instruction.clear()
                self.now_instruction = None

    def break_instructions(self):
        self.clear_instructions()
        if self.now_instruction is not None:
            self.now_instruction.clear()
            self.now_instruction = None

    def compulsorily_clear_instructions(self):
        self.break_instructions()
        for i in self.additional_instructions:
            i.clear()
        self.additional_instructions = []

    def update(self):
        if self.now_instruction is not None:
            if self.now_instruction.end is True:
                self.now_instruction.clear()
                self.now_instruction = None
                if len(self.instruction_waiting_list) == 0:
                    self.waiting = True
                    self.animate_return()

        if self.now_instruction is None:
            if len(self.instruction_waiting_list) > 0:
                self.now_instruction = self.instruction_waiting_list[0]
                del self.instruction_waiting_list[0]
                if self.now_instruction.flag.contain_flag("have_started") is False:
                    self.now_instruction.start(self)
                    self.now_instruction.flag.add_flag("have_started")
            else:
                self.waiting = True

        if self.now_instruction is not None:
            self.now_instruction.update()

        for i in self.additional_instructions:
            if i.end is False:
                i.update()
            else:
                i.clear()
                self.additional_instructions.remove(i)

    def clear(self):
        super().clear()
        self.unit = None
        self.compulsorily_clear_instructions()

