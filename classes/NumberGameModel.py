from json import load, dumps
from .Number import Number
from random import randint


class NumberGameModel:
    def __init__(self, starter_id: str, max_num: int):
        self.words = []
        self.data = {
            'starter_id': starter_id,
            'numbers': [],
            'winner': 0
        }
        self.actual = 4  # randint(1, max_num)

    def add_num(self, num: Number):
        self.data['numbers'].append(num.__dict__)

    def stop(self, winner_id):
        data = load(open('data/guessnumber_hist.json', mode='r', encoding='windows-1251'))
        self.data['winner'] = winner_id
        data['games'].append(self.data)
        f_ = open('data/guessnumber_hist.json', mode='w')
        f_.write(dumps(data, indent=4))
