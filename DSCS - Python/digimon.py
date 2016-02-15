class Digimon(object):

    def __init__(self, name, digivolutions=[], dedigivolutions=[]):
        self.name = name
        self.digivolutions = digivolutions
        self.dedigivolutions = dedigivolutions
        # Digimon.name_index[name].append(self)

    def __str__(self):
        return "%s Digivolves To: %s De-digivolves To: %s" % (self.name, self.digivolutions, self.dedigivolutions)
