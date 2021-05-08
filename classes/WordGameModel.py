from json import load, dumps
from .Word import Word
from utils import get_all_word_games
from os import path


class WordGameModel:
    def __init__(self, starter_id: str):
        self.words = []
        self.data = {
            'id': get_all_word_games()[-1]['id']+1,
            'starter_id': starter_id,
            'words': []
        }

    def add_word(self, word: Word):
        self.data['words'].append(word.__dict__)

    def stop(self):
        data = load(open('data/words_hist.json', mode='r', encoding='windows-1251'))
        data['games'].append(self.data)
        f_ = open('data/words_hist.json', mode='w')
        f_.write(dumps(data, indent=4))
