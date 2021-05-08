from json import load


def get_token():
    return load(open('config.json'))['token']


def get_all_word_games():
    return [i for i in load(open('data/words_hist.json'))['games']]


def get_all_number_games():
    return [i for i in load(open('data/guessnumber_hist.json'))['games']]


def get_word_wins(user_id):
    return len([i['words'][-1]['author_id'] for i in get_all_word_games() if i['words'][-1]['author_id'] == user_id])


def get_num_wins(user_id):
    return len([i['winner'] for i in get_all_number_games() if i['winner'] == user_id])
