from xml.dom.minidom import parse
import xml.dom.minidom


class DataReader:
    data = {}

    def __init__(self, data_name):
        self.data = __class__.read(data_name)

    @classmethod
    def read(cls, data_name):
        for i in cls.data.keys():
            if i == data_name:
                return cls.data[i]

        dom_tree = xml.dom.minidom.parse(data_name)
        collection = dom_tree.documentElement
        cls.data[data_name] = collection
        return collection

    def get(self, name):
        return self.data.getElementsByTagName(name)[0].childNodes[0].data

    def get_attr(self, name):
        pass
