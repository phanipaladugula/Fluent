from app.checkers.base import ExerciseChecker


class MultipleChoiceChecker(ExerciseChecker):
    def check(self, exercise, user_answer: str) -> bool:
        given = self.normalize(user_answer)
        for option in exercise.options:
            if self.normalize(option.text) == given:
                if option.is_correct:
                    return True
                return False
        expected = self.normalize(exercise.correct_answer)
        return expected == given
