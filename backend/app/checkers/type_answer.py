from app.checkers.base import ExerciseChecker


class TypeAnswerChecker(ExerciseChecker):
    def check(self, exercise, user_answer: str) -> bool:
        expected = self.normalize(exercise.correct_answer)
        given = self.normalize(user_answer)
        return expected == given
