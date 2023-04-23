import units.movable_units
import units.buildings
from units.movable_units.soldier import Soldier


class UnitFactory:
    id_dict = dict()
    first_start = False

    @classmethod
    def class_init(cls):
        if cls.first_start is False:
            cls.first_start = True
            cls.id_dict["slim"] = cls.slim
            cls.id_dict["soldier"] = cls.soldier
            cls.id_dict["lin"] = cls.lin
            cls.id_dict["worker"] = cls.worker
            cls.id_dict["ranger"] = cls.ranger
            cls.id_dict["musketeer"] = cls.musketeer
            cls.id_dict["knight"] = cls.knight
            cls.id_dict["minister"] = cls.minister
            cls.id_dict["master"] = cls.master
            cls.id_dict["FlyMachine"] = cls.fly_machine
            cls.id_dict["TruthTeller"] = cls.truth_teller

            cls.id_dict["TestBuilding"] = cls.test_building
            cls.id_dict["base"] = cls.base
            cls.id_dict["TrainingGround"] = cls.training_ground
            cls.id_dict["ResidentialBuilding"] = cls.residential_building
            cls.id_dict["bonfire"] = cls.bonfire
            cls.id_dict["storehouse"] = cls.storehouse
            cls.id_dict["institute"] = cls.institute
            cls.id_dict["CrafterHouse"] = cls.crafter_house
            cls.id_dict["HeroAltar"] = cls.hero_altar
            cls.id_dict["bartizan"] = cls.bartizan
            cls.id_dict["MachineFactory"] = cls.machine_factory
            cls.id_dict["MagicCollege"] = cls.magic_college

    @classmethod
    def truth_teller(cls, x, y):
        return units.movable_units.truth_teller.TruthTeller(x, y)

    @classmethod
    def fly_machine(cls, x, y):
        return units.movable_units.fly_machine.FlyMachine(x, y)

    @classmethod
    def master(cls, x, y):
        return units.movable_units.master.Master(x, y)

    @classmethod
    def knight(cls, x, y):
        return units.movable_units.knight.Knight(x, y)

    @classmethod
    def minister(cls, x, y):
        return units.movable_units.minister.Minister(x, y)

    @classmethod
    def musketeer(cls, x, y):
        return units.movable_units.musketeer.Musketeer(x, y)

    @classmethod
    def ranger(cls, x, y):
        return units.movable_units.ranger.Ranger(x, y)

    @classmethod
    def lin(cls, x, y):
        return units.movable_units.lin.Lin(x, y)

    @classmethod
    def worker(cls, x, y):
        return units.movable_units.worker.Worker(x, y)

    @classmethod
    def soldier(cls, x, y):
        return Soldier(x, y)

    @classmethod
    def slim(cls, x, y):
        return units.movable_units.slim.Slim(x, y)

    @classmethod
    def test_building(cls, x, y):
        return units.buildings.test_building.TestBuilding(x, y)

    @classmethod
    def base(cls, x, y):
        return units.buildings.base.Base(x, y)

    @classmethod
    def training_ground(cls, x, y):
        return units.buildings.training_ground.TrainingGround(x, y)

    @classmethod
    def residential_building(cls, x, y):
        return units.buildings.residential_building.ResidentialBuilding(x, y)

    @classmethod
    def bonfire(cls, x, y):
        return units.buildings.bonfire.Bonfire(x, y)

    @classmethod
    def institute(cls, x, y):
        return units.buildings.institute.Institute(x, y)

    @classmethod
    def storehouse(cls, x, y):
        return units.buildings.storehouse.Storehouse(x, y)

    @classmethod
    def crafter_house(cls, x, y):
        return units.buildings.crafter_house.CrafterHouse(x, y)

    @classmethod
    def hero_altar(cls, x, y):
        return units.buildings.hero_altar.HeroAltar(x, y)

    @classmethod
    def bartizan(cls, x, y):
        return units.buildings.bartizan.Bartizan(x, y)

    @classmethod
    def machine_factory(cls, x, y):
        return units.buildings.machine_factory.MachineFactory(x, y)

    @classmethod
    def magic_college(cls, x, y):
        return units.buildings.magic_college.MagicCollege(x, y)

    @classmethod
    def produce(cls, name, x, y):
        return cls.id_dict[name](x, y)


UnitFactory.class_init()
