from app.checkers.base import ExerciseChecker


class MatchPairsChecker(ExerciseChecker):
    def check(self, exercise, user_answer: str) -> bool:
        expected = self._to_pair_list(exercise.correct_answer)
        given = self._to_pair_list(user_answer)
        if len(expected) != len(given):
            return False

        index = 0
        while index < len(expected):
            if expected[index] != given[index]:
                return False
            index = index + 1
        return True

    def _to_pair_list(self, raw: str):
        pairs = []
        if raw is None:
            return pairs

        chunks = raw.split(";")
        for chunk in chunks:
            if "=" not in chunk:
                continue
            parts = chunk.split("=", 1)
            left = self.normalize(parts[0])
            right = self.normalize(parts[1])
            if left < right:
                key = left + "=" + right
            else:
                key = right + "=" + left
            pairs.append(key)

        pairs.sort()
        return pairs
