from json import load, dumps
from utils import get_all_number_games
from .Number import Number
from random import randint


class NumberGameModel:
    def __init__(self, starter_id: str, max_num: int):
        self.words = []
        self.data = {
            'id': get_all_number_games()[-1]['id']+1,
            'starter_id': starter_id,
            'numbers': [],
            'winner': 0
        }
        self.actual = randint(1, max_num)

    def add_num(self, num: Number):
        self.data['numbers'].append(num.__dict__)

    def stop(self, winner_id):
        data = load(open('data/guessnumber_hist.json', mode='r', encoding='windows-1251'))
        self.data['winner'] = winner_id
        data['games'].append(self.data)
        f_ = open('data/guessnumber_hist.json', mode='w')
        f_.write(dumps(data, indent=4))
