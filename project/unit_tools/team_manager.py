class TeamManager:
    teams = dict()
    player_team = 0
    @classmethod
    def reset_teams(cls):
        cls.teams = dict()

    @classmethod
    def alliance_unidirectional(cls, team1, team2):
        if cls.teams.get(team1) is None:
            cls.teams[team1] = [team2]
        else:
            if team2 not in cls.teams[team1]:
                cls.teams[team1].append(team2)

    @classmethod
    def hostile_unidirectional(cls, team1, team2):
        if cls.teams.get(team1) is None:
            cls.teams[team1] = list()
        else:
            if team2 in cls.teams[team1]:
                cls.teams[team1].remove(team2)

    @classmethod
    def alliance(cls, team1, team2):
        cls.alliance_unidirectional(team1, team2)
        cls.alliance_unidirectional(team2, team1)

    @classmethod
    def hostile(cls, team1, team2):
        cls.hostile_unidirectional(team1, team2)
        cls.hostile_unidirectional(team2, team1)

    @classmethod
    def is_alliance(cls, team1, team2):
        if cls.teams.get(team1) is not None:
            return team2 in cls.teams[team1]
        else:
            cls.teams[team1] = list()
            return False

    @classmethod
    def is_player(cls, team):
        return team == cls.player_team
