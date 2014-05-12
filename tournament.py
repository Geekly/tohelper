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
    def __init__(self, name="Bull Monkey"):
        self.name = name
        self.results = list()

    def __str__(self):
        return self.name

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


class PlayerResult(object):

    def __init__(self, round=0, winresult=Result.tie, armypoints=1000, controlpoints=10):
        #self.player = player
        self.round = round
        self.result = winresult
        self.armypoints = armypoints
        self.controlpoints = controlpoints

    def __str__(self):
        return json.dumps(self, self.__dict__)

    def __repr__(self):
        return repr((self.round, self.result, self.armypoints, self.controlpoints))


class GameResult(object):
    """Represents the result of a game between two players (Pairing) """
    pass


class Pairing(object):
    def __init__(self, player1, player2):
        self.players = (player1, player2)
        self.result = tuple()


class PairingManager(object):
    """Pairing manager will pair players by various factors.
    """
    def __init__(self):
        self.ranking = 0
        pass

    @staticmethod
    def makepairings(playerlist):
        newpairings = grouper( 2, playerlist, '0')
        return newpairings


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
    def __init__(self, numrounds=3, playerlist=list()):
        self.numrounds = numrounds
        self._players = playerlist
        self._rounds = {i: Round(i) for i in range(1,numrounds+1)}
        self.pairingmanager = PairingManager()

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value):
        if value is None:
            raise Exception("Player list is empty")
        self._players = value

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        if value is None:
            raise Exception("Rounds list is empty")
        self._rounds = value

    def pairround(self, roundnum):
        self._rounds[roundnum].pairings = self.pairingmanager.makepairings(self.players)
        return self._rounds[roundnum].pairings


playerlist = [Player(i) for i in string.ascii_uppercase[:9]]  # create 9 players

t = Tournament(3)
t.players = playerlist

p1 = playerlist[0]
p1.results.append( PlayerResult(round=1, winresult=Result.win, armypoints=14, controlpoints=3))
p1.results.append( PlayerResult(round=2, winresult=Result.win, armypoints=13, controlpoints=5))
p1.results.append( PlayerResult(round=3, winresult=Result.win, armypoints=3, controlpoints=0))

print(p1.results)
print(p1.resultsummary())
