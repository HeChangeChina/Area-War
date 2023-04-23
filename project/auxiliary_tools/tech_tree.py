from auxiliary_tools.message_manager import MessageManager


class TechTree:
    tech = dict()
    @classmethod
    def reset_tech(cls):
        cls.tech = dict()

    @classmethod
    def set_level(cls, tech, team, level=1):
        if cls.tech.get(team) is None:
            cls.tech[team] = dict()
        cls.tech[team][tech] = level
        MessageManager.send_message("tech_" + tech + "_change", (tech, cls.tech[team][tech], team))

    @classmethod
    def add_level(cls, tech, team, level=1):
        if cls.tech.get(team) is None:
            cls.tech[team] = dict()
        if cls.tech[team].get(tech) is not None:
            cls.tech[team][tech] += level
        else:
            cls.tech[team][tech] = level
        MessageManager.send_message("tech_" + tech + "_change", (tech, cls.tech[team][tech], team))

    @classmethod
    def reduce_level(cls, tech, team, level=1):
        if cls.tech.get(team) is None:
            cls.tech[team] = dict()
        if cls.tech[team].get(tech) is not None:
            cls.tech[team][tech] -= level
            if cls.tech[team][tech] < 0:
                cls.tech[team][tech] = 0
        else:
            cls.tech[team][tech] = 0
        MessageManager.send_message("tech_" + tech + "_change", (tech, cls.tech[tech], team))

    @classmethod
    def have_tech(cls, team, tech):
        if cls.tech.get(team) is None:
            cls.tech[team] = dict()
        if cls.tech[team].get(tech) is not None:
            return cls.tech[team][tech] > 0
        return False

    @classmethod
    def get_level(cls, team, tech):
        if cls.tech.get(team) is None:
            cls.tech[team] = dict()
        if cls.tech[team].get(tech) is not None:
            return cls.tech[team][tech]
        else:
            return 0
