from json import load, dumps
from random import shuffle


def get_token() -> str:
    return load(open('config.json'))['token']


def get_user_stats(user_id: str) -> dict:
    return load(open('data/stats.json'))[str(user_id)]


def get_words_count(user_id: str) -> int:
    return get_user_stats(user_id)['words']


def get_num_wins(user_id: str) -> int:
    return get_user_stats(user_id)['number_wins']


def get_quiz_wins(user_id: str) -> int:
    return get_user_stats(user_id)['quiz_wins']


def add_user_to_json(user_id: str) -> bool:
    try:
        with open('data/stats.json', 'w+') as f:
            data = load(f)
            data[user_id] = {
                "words": 0,
                "number_wins": 0,
                "quiz_wins": 0
            }
            f.write(dumps(data))
    except:
        return False

    return True


def add_num_wins(user_id: str, wins: int = 1) -> None:
    with open('data/stats.json', 'w+') as f:
        data = load(f)
        data[user_id]['number_wins'] += wins
        f.write(dumps(data))


def add_words(user_id: str, words: int = 1) -> None:
    with open('data/stats.json', 'w+') as f:
        data = load(f)
        data[user_id]['words'] += words
        f.write(dumps(data))


def add_quiz_wins(user_id: str, wins: int = 1) -> None:
    with open('data/stats.json', 'w+') as f:
        data = load(f)
        data[user_id]['quiz_wins'] += wins
        f.write(dumps(data))


def is_city_valid(city: str) -> bool:
    print(load(open('cities.json', 'r+', encoding='utf-8'))['cities'])
    return city in load(open('cities.json', 'r+', encoding='utf-8'))['cities']


def generate_questions(quantity: int) -> list:
    questions = load(open('quiz_questions.json', 'r+', encoding='utf-8'))['questions']
    shuffle(questions)
    return questions[:quantity]
