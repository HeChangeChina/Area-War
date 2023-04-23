from unit_tools.effect import Effect
from unit_tools.filter import Filter
from auxiliary_tools.circle import Circle
from auxiliary_tools.message_manager import MessageManager
from pygame import Rect
from random import sample


class SearchRange(Effect):
    def receive_unit_list(self, units):
        self.data["units"] = units

    def take_effect(self, target, trigger):
        if self.data.get("range") is None:
            print("Warning: effect 'SearchRange' got the wrong data, 'range' is missing.")
            return
        elif self.data.get("effect") is None:
            print("Warning: effect 'SearchRange' got the wrong data, 'effect' is missing.")
            return
        if self.data.get("circle") is None:
            self.data["circle"] = True
        if self.data.get("max_amount") is None:
            self.data["max_amount"] = 9999
        if self.data.get("target_included") is None:
            self.data["target_included"] = True
        if self.data.get("required_flag") is None:
            self.data["required_flag"] = ["unit"]
        if self.data.get("excluded_flag") is None:
            self.data["excluded_flag"] = []
        if self.data.get("included_flag") is None:
            self.data["included_flag"] = []

        center_x = target[0] if type(target) is list or type(
            target) is tuple else target.c_rect.left + target.c_rect.width / 2
        center_y = target[1] if type(target) is list or type(
            target) is tuple else target.c_rect.top + target.c_rect.height / 2

        if self.data["circle"]:
            x = center_x - self.data["range"]
            y = center_y - self.data["range"]
            coll = Circle(x, y, self.data["range"])
        else:
            coll = Rect(center_x - self.data["range"], 0, self.data["range"] * 2, 1080)
        MessageManager.send_message("search_range", [coll, self])
        if self.data["target_included"] is False:
            for i in self.data["units"]:
                if i == target:
                    self.data["units"].remove(i)
                    break

        unit_filter = Filter(trigger, self.data["required_flag"], self.data["excluded_flag"], self.data["included_flag"])
        filter_list = list()
        for i in self.data["units"]:
            if unit_filter.filter(i):
                filter_list.append(i)
        if len(filter_list) > self.data["max_amount"]:
            filter_list = sample(filter_list, self.data["max_amount"])
        for i in filter_list:
            self.data["effect"].take_effect(i, trigger)
        unit_filter.clear()
        self.data["units"] = list()


