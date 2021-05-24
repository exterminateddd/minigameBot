from json import load, dumps
from .Word import Word
from utils import add_user_to_json
from os import path


class WordGameModel:
    def __init__(self, starter_id: str):
        self.words = []
        self.starter = starter_id

    def add_word(self, word: Word):
        self.words.append(word.__dict__)

    def stop(self):
        data = load(open('data/stats.json', mode='r', encoding='windows-1251'))
        try:
            if str(self.words[-1]['author_id']) not in data:
                add_user_to_json(str(self.words[-1]['author_id']))
                data[str(self.words[-1]['author_id'])] = {
                    "words": 0,
                    "number_wins": 0,
                    "quiz_wins": 0
                }
            data[str(self.words[-1]['author_id'])]['words'] += 1
        except:
            pass
        f_ = open('data/stats.json', mode='w')
        f_.write(dumps(data, indent=4))
