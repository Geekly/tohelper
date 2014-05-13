__author__ = 'geekly'

import string
import json
from random import shuffle
from enum import Enum
from itertools import zip_longest


def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Result(Enum):
    win = 1
    lose = 0
    tie = 0


class Player(object):
    def __init__(self, name="Bull Monkey" ):
        self.name = name
        self.results = []
        self.sos = 0
        self.record = None
        self.locale = None

    def __str__(self):
        return self.name

    def addresult(self, playerresult):
        assert isinstance(playerresult, PlayerResult)
        self.results.append(playerresult)

    def resultsummary(self):
        """Add up the player results from the result list
            summary = (tournament score, SOS, armypoints, controlpoints)
        """
        playersummary = [0, 0, 0, 0]
        for roundresult in self.results:
            playersummary[0] += roundresult.result.value
            #playersummary[1] += roundresult.sos
            playersummary[2] += roundresult.armypoints
            playersummary[3] += roundresult.controlpoints

        #todo: calcualate SOS

        return playersummary

    def __repr__(self):
        return self.name


class PlayerResult(object):
    def __init__(self, opponent, round=0, winresult=Result.tie, armypoints=1000, controlpoints=10):
        #self.player = player
        self.round = round
        self.opponent = opponent
        self.result = winresult
        self.armypoints = armypoints
        self.controlpoints = controlpoints

    def __str__(self):
        return json.dumps(self, self.__dict__)

    def __repr__(self):
        return "(Round: {round}, Result: {result}, Control Points {cp}, Army Points: {ap})".format(
            round=self.round, result=self.result, cp=self.controlpoints, ap=self.armypoints)
        #return repr((self.round, self.result, self.armypoints, self.controlpoints))


#todo: this doesn't make sense
class GameResult(object):
    """Represents the result of a game between two players (Pairing) """

    def __init__(self, pairing):
        self._paring = pairing


#todo:  should Pairing own gameresult or vice versa?
class Pairing(object):
    def __init__(self, player1, player2):
        self.players = (player1, player2)
        self.result = tuple()

    def __repr__(self):
        return (repr(self.players[0], repr(self.player[1])))

class PairingManager(object):
    """Pairing manager will pair players by various factors.
    """

    def __init__(self):
        self.ranking = 0
        pass

    @staticmethod
    def makepairings(players, firstround=False):
        """If first round is true, pair randomly

            Prevent pairing in first round based on locale
        """
        templist = players.copy()
        if firstround:
            shuffle(templist)
        newpairings = grouper(2, templist, Player(name="Buy"))
        return [pairing for pairing in newpairings]


class Round(object):
    """Round of a tournament.

        _pairings: list() of the round's pairings
        roundnum: round number

    """

    def __init__(self, roundnum):
        self._pairings = list()
        self.roundnum = roundnum
        pass

    @property
    def pairings(self):
        return self._pairings

    @pairings.setter
    def pairings(self, pairings):
        self._pairings = pairings


class Tournament(object):
    """Represents a tournament

        numrounds: number of rounds (also size of _rounds)
        _players: list() of players
        _rounds: list() of rounds
        pairingmanager: the PairingManager

    """

    def __init__(self, numrounds=3):
        self.numrounds = numrounds
        self._players = []  # first player is the buy
        self._rounds = {i: Round(i) for i in range(1, numrounds + 1)}
        self.currentround = self._rounds[1]
        self.pairingmanager = PairingManager()

    @property
    def players(self):
        return self._players

    @property
    def rounds(self):
        return self._rounds

    def startround(self, roundnum):
        """
        """
        assert (0 < roundnum) and (roundnum <= self.numrounds), "Round {number} does not exist".format(number=roundnum)
        self.currentround = self._rounds[roundnum]
        return self.pairround(roundnum)

    def endcurrentround(self):
        self.__endround(self.currentround)

    def __endround(self, roundnum):
        """Update SOS for the round and set next round

        """
        #update SOS for each player
        assert (0 < roundnum) and (roundnum <= self.numrounds), "Round {number} does not exist".format(number=roundnum)
        for player in playerlist:
            #todo: calculate SOS
            pass
        if roundnum < self.numrounds:
            self.currentround += roundnum

    def pairround(self, roundnum):
        assert (0 < roundnum) and (roundnum <= self.numrounds), "Round {number} does not exist".format(number=roundnum)

        print("Pairing round:", roundnum)
        self._rounds[roundnum].pairings = self.pairingmanager.makepairings(self.players, roundnum == 1)
        return self._rounds[roundnum].pairings


playerlist = [Player("Player" + i) for i in string.ascii_uppercase[:5]]  # create 9 players

t = Tournament(3)
t.players.extend(playerlist)

t.startround(1)


#pairings = PairingManager.makepairings(t.players)

#print([p for p in pairings])

#pairings = PairingManager.makepairings(t.players, firstround=True)

#for p in pairings:
#    print(p)

#pairs = [p for p in pairings]
#print(pairs)
t.pairround(2)
t.pairround(3)

for roundnum, round in t._rounds.items():
    print( roundnum, round.pairings )
"""
p1 = playerlist[0]
p2 = playerlist[1]
p3 = playerlist[2]
p4 = playerlist[3]
p5 = playerlist[4]

for pair in pairings:
    print(pair)
    pair[0].results.append(PlayerResult(pair[1], round=1, winresult=Result.win, armypoints=14, controlpoints=3))
    pair[1].results.append(PlayerResult(pair[0], round=1, winresult=Result.lose, armypoints=14, controlpoints=3))
    pair[0].results.append(PlayerResult(pair[1], round=2, winresult=Result.win, armypoints=14, controlpoints=3))
    pair[1].results.append(PlayerResult(pair[0], round=2, winresult=Result.lose, armypoints=14, controlpoints=3))
    pair[0].results.append(PlayerResult(pair[1], round=3, winresult=Result.win, armypoints=14, controlpoints=3))
    pair[1].results.append(PlayerResult(pair[0], round=3, winresult=Result.lose, armypoints=14, controlpoints=3))

print(p1.results)
print(p1.resultsummary())
print(p2.results)
print(p2.resultsummary())
"""