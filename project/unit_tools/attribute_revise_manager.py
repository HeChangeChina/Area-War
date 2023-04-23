from base import Base


class AttributeReviseManager(Base):
    def __init__(self):
        super().__init__()
        self.if_clear = False
        self.revise_list = []
        self.attribute_list = list()

    def set_attribute_list(self, attr_dict):
        self.attribute_list = list()
        for i in attr_dict:
            self.attribute_list.append(i)

        for i in self.revise_list:
            i.set_attribute_list(self.attribute_list)

    def add(self, attribute_revise):
        self.revise_list.append(attribute_revise)
        attribute_revise.set_attribute_list(self.attribute_list)

    def attribute_update(self, attribute_list):
        for i in self.revise_list:
            if i.if_clear is True:
                self.revise_list.remove(i)
        for i in self.revise_list:
            attribute_list = i.attribute_update(attribute_list)
        return attribute_list

    def clear(self):
        super().clear()
        self.if_clear = True
        for i in self.revise_list:
            i.clear()
        self.revise_list = []
