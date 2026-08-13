from app.checkers.base import ExerciseChecker
from app.checkers.multiple_choice import MultipleChoiceChecker
from app.checkers.translate import TranslateChecker
from app.checkers.match_pairs import MatchPairsChecker
from app.checkers.fill_blank import FillBlankChecker
from app.checkers.type_answer import TypeAnswerChecker


class ExerciseCheckerFactory:
    def get_checker(self, exercise_type: str) -> ExerciseChecker:
        if exercise_type == "multiple_choice":
            return MultipleChoiceChecker()
        if exercise_type == "translate":
            return TranslateChecker()
        if exercise_type == "match_pairs":
            return MatchPairsChecker()
        if exercise_type == "fill_blank":
            return FillBlankChecker()
        if exercise_type == "type_answer":
            return TypeAnswerChecker()
        return TypeAnswerChecker()
