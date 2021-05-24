from utils import add_quiz_wins, generate_questions


class QuizGameModel:
    def __init__(self, questions):
        self.questions = [*generate_questions(questions)]
        self.current_question = 0
        self.answers = []

    def add_answer(self, user):
        self.answers.append(user.id)

        if self.current_question != len(self.questions):
            self.current_question += 1

    def get_winner(self):
        return max(set(self.answers), key=self.answers.count)

    def end(self):
        add_quiz_wins(self.get_winner(), 1)
