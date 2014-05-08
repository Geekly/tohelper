__author__ = 'geekly'

import string
from random import shuffle
from itertools import zip_longest


def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Round(object):
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


class Player(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class PlayerResult(object):
    def __init__(self, player):
        self._player = player
        self._round = 0


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


class Tournament(object):
    """Represents a tournament
    """
    def __init__(self, numrounds):
        self.numrounds = numrounds
        self._players = list()
        self._rounds = {i:Round(i) for i in range(1,numrounds+1)}
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



playerlist = [ Player(i) for i in string.ascii_uppercase[:9] ] # create 8 players

t = Tournament(3)
t.players = playerlist
pair = t.pairround(1)

for p in pair:
    print(*p)