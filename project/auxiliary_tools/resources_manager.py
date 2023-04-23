class ResourcesManager:
    resources_dict = dict()

    @classmethod
    def reset(cls):
        cls.resources_dict = dict()

    @classmethod
    def add_resources(cls, resources, value, team):
        if cls.resources_dict.get(team) is None:
            cls.resources_dict[team] = dict()
        if cls.resources_dict[team].get(resources) is None:
            cls.resources_dict[team][resources] = 0
        cls.resources_dict[team][resources] += value

    @classmethod
    def get_resources(cls, resources, team):
        if cls.resources_dict.get(team) is None:
            cls.resources_dict[team] = dict()
        if cls.resources_dict[team].get(resources) is None:
            result = 0
        else:
            result = cls.resources_dict[team].get(resources)
        return result
