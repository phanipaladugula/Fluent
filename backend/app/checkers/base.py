class ExerciseChecker:
    def check(self, exercise, user_answer: str) -> bool:
        raise NotImplementedError

    def normalize(self, text: str) -> str:
        if text is None:
            return ""
        cleaned = text.strip().lower()
        cleaned = cleaned.replace("á", "a")
        cleaned = cleaned.replace("é", "e")
        cleaned = cleaned.replace("í", "i")
        cleaned = cleaned.replace("ó", "o")
        cleaned = cleaned.replace("ú", "u")
        cleaned = cleaned.replace("ñ", "n")
        cleaned = cleaned.replace("ü", "u")
        cleaned = cleaned.replace("'", "")
        extra_spaces = " ".join(cleaned.split())
        return extra_spaces
