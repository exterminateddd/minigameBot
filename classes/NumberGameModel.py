from json import load, dumps
from .Number import Number
from random import randint
from utils import add_num_wins


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
        add_num_wins(winner_id, 1)
