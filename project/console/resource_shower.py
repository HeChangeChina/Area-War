from base import Base
from auxiliary_tools.resources_manager import ResourcesManager
from unit_tools.team_manager import TeamManager
from display.atlas import Atlas
from display.font import FontSurface
from pygame.rect import Rect


class ResourceShower(Base):
    def __init__(self):
        super().__init__()
        self.gold_before = -999
        self.wood_before = -999
        self.population_before = -999
        self.max_population_before = -999
        self.gold_surface = Atlas.load("./data/img/console", "gold")["defeat"][0][0]
        self.wood_surface = Atlas.load("./data/img/console", "wood")["defeat"][0][0]
        self.population_surface = Atlas.load("./data/img/console", "population")["defeat"][0][0]
        self.resource_shower_bg = Atlas.load("./data/img/console", "ResourceShowerBG")["defeat"][0][0]
        self.gold_text_surface = FontSurface(text="0", size=18).surface
        self.wood_text_surface = FontSurface(text="0", size=18).surface
        self.population_text_surface = FontSurface(text="0/0", size=18).surface

    def update(self):
        team = TeamManager.player_team
        gold_number = ResourcesManager.get_resources("gold", team)
        wood_number = ResourcesManager.get_resources("wood", team)
        population_number = ResourcesManager.get_resources("population", team)
        max_population_number = ResourcesManager.get_resources("max_population", team)

        if gold_number != self.gold_before:
            self.gold_text_surface = FontSurface(text=str(int(gold_number)), size=20).surface
            self.gold_before = gold_number
        if wood_number != self.wood_before:
            self.wood_text_surface = FontSurface(text=str(int(wood_number)), size=20).surface
            self.wood_before = wood_number
        if population_number != self.population_before or max_population_number != self.max_population_before:
            text = str(int(population_number)) + "/" + str(int(max_population_number))
            color = (255, 255, 255) if population_number <= max_population_number else (200, 100, 100)
            self.population_text_surface = FontSurface(text=text, size=20, color=color).surface
            self.population_before = population_number
            self.max_population_before = max_population_number

    def get_surface(self):
        surface_list = list()
        rect_gold = Rect(1800, 20, 20, 20)
        rect_wood = Rect(1700, 20, 20, 20)
        rect_population = Rect(1600, 20, 20, 20)
        rect_gold_text = Rect(1790 - self.gold_text_surface.get_width(), 20, self.gold_text_surface.get_width(), 20)
        rect_wood_text = Rect(1690 - self.wood_text_surface.get_width(), 20, self.wood_text_surface.get_width(), 20)
        rect_population_text = Rect(1590 - self.population_text_surface.get_width(), 20, self.population_text_surface.get_width(), 20)
        resource_bg = Rect(1480, 0, 500, 40)
        surface_list.append([self.resource_shower_bg, resource_bg])
        surface_list.append([self.gold_surface, rect_gold])
        surface_list.append([self.wood_surface, rect_wood])
        surface_list.append([self.population_surface, rect_population])
        surface_list.append([self.gold_text_surface, rect_gold_text])
        surface_list.append([self.wood_text_surface, rect_wood_text])
        surface_list.append([self.population_text_surface, rect_population_text])
        return surface_list
