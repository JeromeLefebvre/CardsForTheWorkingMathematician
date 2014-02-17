class Game(object):
    RULES = {'standonsoft17':False,'bjack_pays':(6,5), 'surrender':False}

    def __init__(self, rules = RULES, withplayer=False):
        self.players=[]
        self.rules=rules
        if withplayer:
            self.addPlayer(NormalPlayer(100,"Carlos"))

    def addPlayer(self, player):
        self.players.append(player)

    def runUI(self):
        #Maybe this will be in charge of flow control
        pass