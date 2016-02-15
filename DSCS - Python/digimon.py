from enum import Enum


class Stage(Enum):
    none = 0
    baby = 1
    in_training = 2
    rookie = 3
    champion = 4
    ultimate = 5
    mega = 6
    super_ultimate = 7
    armor = 8


class Type(Enum):
    free = 0
    data = 1
    virus = 2
    vaccine = 3


class Element(Enum):
    none = 0
    fire = 1
    plant = 2
    water = 3
    thunder = 4
    wind = 5
    earth = 6
    light = 7
    dark = 8


class Digimon(object):

    def __init__(self, name, digivolutions=[], dedigivolutions=[], skills=[], stage=Stage.none):
        self.name = name
        self.digivolutions = digivolutions
        self.dedigivolutions = dedigivolutions
        self.skills = skills
        self.stage = stage
        # Digimon.name_index[name].append(self)

    def __str__(self):
        return "%s Digivolves To: %s\nDe-digivolves To: %s\nSkills: %s" % (self.name, self.digivolutions, self.dedigivolutions, self.skills)
