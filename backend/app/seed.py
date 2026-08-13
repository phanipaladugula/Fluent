from datetime import datetime, date
import random

from sqlalchemy.orm import Session

from app.config import config
from app.models.user import User
from app.models.course import Course, Unit, Skill, Lesson, Exercise, ExerciseOption
from app.models.progress import UserSkillProgress, UserLessonCompletion, XpEvent
from app.models.achievement import Achievement, UserAchievement


class CourseSeeder:
    def __init__(self, db: Session):
        self.db = db

    def run(self):
        existing = self.db.query(User).filter(User.username == "alex").first()
        if existing is not None:
            return

        self._create_users()
        self._create_achievements()
        course = self._create_course()
        unit1 = self._create_unit(
            course.id,
            "Unit 1",
            "Order coffee, say hello, and introduce yourself.",
            1,
            "#58CC02",
        )
        unit2 = self._create_unit(
            course.id,
            "Unit 2",
            "Talk about food and animals around you.",
            2,
            "#1CB0F6",
        )
        unit3 = self._create_unit(
            course.id,
            "Unit 3",
            "Find your way and name common places.",
            3,
            "#CE82FF",
        )

        greetings = self._create_skill(unit1.id, "Greetings", "Hello, goodbye, and polite words.", 1, "wave")
        intros = self._create_skill(unit1.id, "Introductions", "Share your name and who you are.", 2, "id")
        phrases = self._create_skill(unit1.id, "Phrases", "Useful everyday Spanish phrases.", 3, "chat")
        food = self._create_skill(unit2.id, "Food", "Order and name common foods.", 1, "apple")
        animals = self._create_skill(unit2.id, "Animals", "Name pets and animals.", 2, "paw")
        places = self._create_skill(unit3.id, "Places", "Talk about the city around you.", 1, "pin")

        greetings_lesson = self._seed_greetings_lesson(greetings.id)
        self._seed_introductions_lesson(intros.id)
        self._seed_phrases_lesson(phrases.id)
        self._seed_food_lesson(food.id)
        self._seed_animals_lesson(animals.id)
        self._seed_places_lesson(places.id)

        self._seed_alex_progress(greetings.id, greetings_lesson.id)
        self.db.commit()

    def _create_users(self):
        today = date.today()
        now = datetime.utcnow()

        alex = User(
            username="alex",
            display_name="Alex",
            total_xp=120,
            gems=450,
            hearts=config.MAX_HEARTS,
            max_hearts=config.MAX_HEARTS,
            last_heart_at=now,
            streak_count=3,
            last_activity_date=today,
            daily_xp=10,
            daily_goal_xp=config.DAILY_GOAL_XP,
            last_xp_date=today,
        )
        bella = User(
            username="bella",
            display_name="Bella",
            total_xp=280,
            gems=200,
            hearts=5,
            max_hearts=5,
            last_heart_at=now,
            streak_count=12,
            last_activity_date=today,
            daily_xp=30,
            daily_goal_xp=20,
            last_xp_date=today,
        )
        carlos = User(
            username="carlos",
            display_name="Carlos",
            total_xp=420,
            gems=800,
            hearts=5,
            max_hearts=5,
            last_heart_at=now,
            streak_count=21,
            last_activity_date=today,
            daily_xp=40,
            daily_goal_xp=20,
            last_xp_date=today,
        )
        dana = User(
            username="dana",
            display_name="Dana",
            total_xp=95,
            gems=80,
            hearts=5,
            max_hearts=5,
            last_heart_at=now,
            streak_count=2,
            last_activity_date=today,
            daily_xp=10,
            daily_goal_xp=20,
            last_xp_date=today,
        )
        eli = User(
            username="eli",
            display_name="Eli",
            total_xp=60,
            gems=40,
            hearts=5,
            max_hearts=5,
            last_heart_at=now,
            streak_count=1,
            last_activity_date=today,
            daily_xp=0,
            daily_goal_xp=20,
            last_xp_date=today,
        )
        self.db.add(alex)
        self.db.add(bella)
        self.db.add(carlos)
        self.db.add(dana)
        self.db.add(eli)
        self.db.flush()

    def _create_achievements(self):
        first_lesson = Achievement(
            code="first_lesson",
            title="First Lesson",
            description="Complete your first lesson.",
            icon="star",
        )
        streak_starter = Achievement(
            code="streak_starter",
            title="Streak Starter",
            description="Reach a 3-day streak.",
            icon="fire",
        )
        xp_hunter = Achievement(
            code="xp_hunter",
            title="XP Hunter",
            description="Earn 50 total XP.",
            icon="zap",
        )
        unit_finisher = Achievement(
            code="unit_finisher",
            title="Unit Finisher",
            description="Complete every skill in a unit.",
            icon="flag",
        )
        perfect_lesson = Achievement(
            code="perfect_lesson",
            title="Perfect Lesson",
            description="Finish a lesson without losing a heart.",
            icon="heart",
        )
        self.db.add(first_lesson)
        self.db.add(streak_starter)
        self.db.add(xp_hunter)
        self.db.add(unit_finisher)
        self.db.add(perfect_lesson)
        self.db.flush()

    def _create_course(self):
        course = Course(
            language_code="es",
            title="Spanish",
            from_language="English",
        )
        self.db.add(course)
        self.db.flush()
        return course

    def _create_unit(self, course_id, title, description, order_index, color):
        unit = Unit(
            course_id=course_id,
            title=title,
            description=description,
            order_index=order_index,
            color=color,
        )
        self.db.add(unit)
        self.db.flush()
        return unit

    def _create_skill(self, unit_id, title, description, order_index, icon):
        skill = Skill(
            unit_id=unit_id,
            title=title,
            description=description,
            order_index=order_index,
            icon=icon,
            max_crowns=5,
        )
        self.db.add(skill)
        self.db.flush()
        return skill

    def _create_lesson(self, skill_id, title, order_index):
        lesson = Lesson(
            skill_id=skill_id,
            title=title,
            order_index=order_index,
            xp_reward=config.LESSON_XP,
        )
        self.db.add(lesson)
        self.db.flush()
        return lesson

    def _create_exercise(self, lesson_id, exercise_type, prompt, correct_answer, order_index):
        exercise = Exercise(
            lesson_id=lesson_id,
            type=exercise_type,
            prompt=prompt,
            correct_answer=correct_answer,
            order_index=order_index,
        )
        self.db.add(exercise)
        self.db.flush()
        return exercise

    def _add_option(self, exercise_id, text, is_correct, pair_group, side, order_index):
        option = ExerciseOption(
            exercise_id=exercise_id,
            text=text,
            is_correct=is_correct,
            pair_group=pair_group,
            side=side,
            order_index=order_index,
        )
        self.db.add(option)

    def _add_mcq_options(self, exercise_id, choices, correct_text):
        mixed = list(choices)
        random.shuffle(mixed)
        index = 1
        for choice in mixed:
            is_correct = False
            if choice == correct_text:
                is_correct = True
            self._add_option(exercise_id, choice, is_correct, None, None, index)
            index = index + 1

    def _add_word_bank(self, exercise_id, words):
        mixed = list(words)
        random.shuffle(mixed)
        index = 1
        for word in mixed:
            self._add_option(exercise_id, word, False, None, None, index)
            index = index + 1

    def _add_match_pair(self, exercise_id, left_text, right_text, group, start_index):
        self._add_option(exercise_id, left_text, False, group, "left", start_index)
        self._add_option(exercise_id, right_text, False, group, "right", start_index + 1)

    def _seed_greetings_lesson(self, skill_id):
        lesson = self._create_lesson(skill_id, "Say hello", 1)

        ex1 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "Hola" mean?',
            "Hello",
            1,
        )
        self._add_mcq_options(ex1.id, ["Please", "Water", "Hello", "Thanks"], "Hello")

        ex2 = self._create_exercise(
            lesson.id,
            "translate",
            "Translate this to Spanish: Hello",
            "Hola",
            2,
        )
        self._add_word_bank(ex2.id, ["Hola", "Adiós", "Casa", "El"])

        ex3 = self._create_exercise(
            lesson.id,
            "match_pairs",
            "Match the pairs",
            "Hola=Hello;Adiós=Goodbye;Gracias=Thanks",
            3,
        )
        self._add_match_pair(ex3.id, "Hola", "Hello", 1, 1)
        self._add_match_pair(ex3.id, "Adiós", "Goodbye", 2, 3)
        self._add_match_pair(ex3.id, "Gracias", "Thanks", 3, 5)

        ex4 = self._create_exercise(
            lesson.id,
            "fill_blank",
            "Complete the phrase: Buenos ____",
            "días",
            4,
        )
        self._add_mcq_options(ex4.id, ["días", "casa", "perro", "agua"], "días")

        self._create_exercise(
            lesson.id,
            "type_answer",
            'Type the Spanish word for "please"',
            "por favor",
            5,
        )

        ex6 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "Buenas noches" mean?',
            "Good night",
            6,
        )
        self._add_mcq_options(
            ex6.id,
            ["Good night", "Good morning", "See you later", "How are you"],
            "Good night",
        )

        ex7 = self._create_exercise(
            lesson.id,
            "translate",
            "Translate this to Spanish: Thank you",
            "Gracias",
            7,
        )
        self._add_word_bank(ex7.id, ["Gracias", "Hola", "Perro", "Yo"])

        return lesson

    def _seed_introductions_lesson(self, skill_id):
        lesson = self._create_lesson(skill_id, "Introduce yourself", 1)

        ex1 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "Me llamo" mean?',
            "My name is",
            1,
        )
        self._add_mcq_options(
            ex1.id,
            ["I am hungry", "See you soon", "My name is", "Good afternoon"],
            "My name is",
        )

        ex2 = self._create_exercise(
            lesson.id,
            "translate",
            "Translate this to Spanish: I am a boy",
            "Yo soy un niño",
            2,
        )
        self._add_word_bank(ex2.id, ["Yo", "soy", "un", "niño", "casa", "agua"])

        ex3 = self._create_exercise(
            lesson.id,
            "match_pairs",
            "Match the pairs",
            "Yo=I;Tú=You;Él=He;Ella=She",
            3,
        )
        self._add_match_pair(ex3.id, "Yo", "I", 1, 1)
        self._add_match_pair(ex3.id, "Tú", "You", 2, 3)
        self._add_match_pair(ex3.id, "Él", "He", 3, 5)
        self._add_match_pair(ex3.id, "Ella", "She", 4, 7)

        ex4 = self._create_exercise(
            lesson.id,
            "fill_blank",
            "Complete the sentence: Yo ____ María.",
            "soy",
            4,
        )
        self._add_mcq_options(ex4.id, ["soy", "tengo", "voy", "como"], "soy")

        self._create_exercise(
            lesson.id,
            "type_answer",
            'Type the Spanish word for "I am"',
            "soy",
            5,
        )

        ex6 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "¿Cómo te llamas?" mean?',
            "What is your name?",
            6,
        )
        self._add_mcq_options(
            ex6.id,
            ["What is your name?", "How old are you?", "Where are you from?", "How are you?"],
            "What is your name?",
        )

        return lesson

    def _seed_phrases_lesson(self, skill_id):
        lesson = self._create_lesson(skill_id, "Useful phrases", 1)

        ex1 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "¿Cómo estás?" mean?',
            "How are you?",
            1,
        )
        self._add_mcq_options(
            ex1.id,
            ["What time is it?", "I am sorry", "How are you?", "Where is the station?"],
            "How are you?",
        )

        ex2 = self._create_exercise(
            lesson.id,
            "translate",
            "Translate this to Spanish: See you later",
            "Hasta luego",
            2,
        )
        self._add_word_bank(ex2.id, ["Hasta", "luego", "Hola", "Casa"])

        ex3 = self._create_exercise(
            lesson.id,
            "match_pairs",
            "Match the pairs",
            "Por favor=Please;De nada=You're welcome;Lo siento=I am sorry",
            3,
        )
        self._add_match_pair(ex3.id, "Por favor", "Please", 1, 1)
        self._add_match_pair(ex3.id, "De nada", "You're welcome", 2, 3)
        self._add_match_pair(ex3.id, "Lo siento", "I am sorry", 3, 5)

        ex4 = self._create_exercise(
            lesson.id,
            "fill_blank",
            "Complete the phrase: Hasta ____",
            "luego",
            4,
        )
        self._add_mcq_options(ex4.id, ["luego", "perro", "mesa", "leche"], "luego")

        self._create_exercise(
            lesson.id,
            "type_answer",
            'Type the Spanish for "you\'re welcome"',
            "de nada",
            5,
        )

        ex6 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "No entiendo" mean?',
            "I do not understand",
            6,
        )
        self._add_mcq_options(
            ex6.id,
            ["I do not understand", "I am tired", "I want water", "Good luck"],
            "I do not understand",
        )

        return lesson

    def _seed_food_lesson(self, skill_id):
        lesson = self._create_lesson(skill_id, "At the cafe", 1)

        ex1 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "el pan" mean?',
            "bread",
            1,
        )
        self._add_mcq_options(ex1.id, ["cheese", "apple", "bread", "fish"], "bread")

        ex2 = self._create_exercise(
            lesson.id,
            "translate",
            "Translate this to Spanish: I want water",
            "Yo quiero agua",
            2,
        )
        self._add_word_bank(ex2.id, ["Yo", "quiero", "agua", "pan", "gato"])

        ex3 = self._create_exercise(
            lesson.id,
            "match_pairs",
            "Match the pairs",
            "manzana=apple;queso=cheese;leche=milk;café=coffee",
            3,
        )
        self._add_match_pair(ex3.id, "manzana", "apple", 1, 1)
        self._add_match_pair(ex3.id, "queso", "cheese", 2, 3)
        self._add_match_pair(ex3.id, "leche", "milk", 3, 5)
        self._add_match_pair(ex3.id, "café", "coffee", 4, 7)

        ex4 = self._create_exercise(
            lesson.id,
            "fill_blank",
            "Complete the sentence: Quiero un ____",
            "café",
            4,
        )
        self._add_mcq_options(ex4.id, ["café", "libro", "zapato", "parque"], "café")

        self._create_exercise(
            lesson.id,
            "type_answer",
            'Type the Spanish word for "apple"',
            "manzana",
            5,
        )

        ex6 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "Tengo hambre" mean?',
            "I am hungry",
            6,
        )
        self._add_mcq_options(
            ex6.id,
            ["I am hungry", "I am thirsty", "I am cold", "The food is good"],
            "I am hungry",
        )

        return lesson

    def _seed_animals_lesson(self, skill_id):
        lesson = self._create_lesson(skill_id, "Pets and animals", 1)

        ex1 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "el gato" mean?',
            "the cat",
            1,
        )
        self._add_mcq_options(ex1.id, ["the dog", "the bird", "the cat", "the horse"], "the cat")

        ex2 = self._create_exercise(
            lesson.id,
            "translate",
            "Translate this to Spanish: the dog",
            "el perro",
            2,
        )
        self._add_word_bank(ex2.id, ["el", "perro", "gato", "casa"])

        ex3 = self._create_exercise(
            lesson.id,
            "match_pairs",
            "Match the pairs",
            "gato=cat;perro=dog;pájaro=bird;caballo=horse",
            3,
        )
        self._add_match_pair(ex3.id, "gato", "cat", 1, 1)
        self._add_match_pair(ex3.id, "perro", "dog", 2, 3)
        self._add_match_pair(ex3.id, "pájaro", "bird", 3, 5)
        self._add_match_pair(ex3.id, "caballo", "horse", 4, 7)

        ex4 = self._create_exercise(
            lesson.id,
            "fill_blank",
            "Complete the sentence: El ____ es grande.",
            "caballo",
            4,
        )
        self._add_mcq_options(ex4.id, ["caballo", "leche", "mesa", "hola"], "caballo")

        self._create_exercise(
            lesson.id,
            "type_answer",
            'Type the Spanish word for "bird"',
            "pájaro",
            5,
        )

        ex6 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "Me gusta el gato" mean?',
            "I like the cat",
            6,
        )
        self._add_mcq_options(
            ex6.id,
            ["I like the cat", "I have a dog", "The bird is small", "The horse runs"],
            "I like the cat",
        )

        return lesson

    def _seed_places_lesson(self, skill_id):
        lesson = self._create_lesson(skill_id, "Around town", 1)

        ex1 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "la casa" mean?',
            "the house",
            1,
        )
        self._add_mcq_options(ex1.id, ["the park", "the house", "the store", "the school"], "the house")

        ex2 = self._create_exercise(
            lesson.id,
            "translate",
            "Translate this to Spanish: the school",
            "la escuela",
            2,
        )
        self._add_word_bank(ex2.id, ["la", "escuela", "casa", "el"])

        ex3 = self._create_exercise(
            lesson.id,
            "match_pairs",
            "Match the pairs",
            "casa=house;escuela=school;parque=park;tienda=store",
            3,
        )
        self._add_match_pair(ex3.id, "casa", "house", 1, 1)
        self._add_match_pair(ex3.id, "escuela", "school", 2, 3)
        self._add_match_pair(ex3.id, "parque", "park", 3, 5)
        self._add_match_pair(ex3.id, "tienda", "store", 4, 7)

        ex4 = self._create_exercise(
            lesson.id,
            "fill_blank",
            "Complete the sentence: Voy al ____",
            "parque",
            4,
        )
        self._add_mcq_options(ex4.id, ["parque", "queso", "gato", "leche"], "parque")

        self._create_exercise(
            lesson.id,
            "type_answer",
            'Type the Spanish word for "store"',
            "tienda",
            5,
        )

        ex6 = self._create_exercise(
            lesson.id,
            "multiple_choice",
            'What does "¿Dónde está el parque?" mean?',
            "Where is the park?",
            6,
        )
        self._add_mcq_options(
            ex6.id,
            ["Where is the park?", "How much is it?", "What is your name?", "I am at school"],
            "Where is the park?",
        )

        return lesson

    def _seed_alex_progress(self, greetings_skill_id, greetings_lesson_id):
        alex = self.db.query(User).filter(User.username == "alex").first()
        now = datetime.utcnow()

        progress = UserSkillProgress(
            user_id=alex.id,
            skill_id=greetings_skill_id,
            crowns=1,
            is_unlocked=True,
        )
        self.db.add(progress)

        completion = UserLessonCompletion(
            user_id=alex.id,
            lesson_id=greetings_lesson_id,
            completed_at=now,
            xp_earned=10,
        )
        self.db.add(completion)

        xp_event = XpEvent(
            user_id=alex.id,
            amount=10,
            reason="lesson_complete",
            created_at=now,
        )
        self.db.add(xp_event)

        first_lesson = self.db.query(Achievement).filter(Achievement.code == "first_lesson").first()
        streak_starter = self.db.query(Achievement).filter(Achievement.code == "streak_starter").first()
        xp_hunter = self.db.query(Achievement).filter(Achievement.code == "xp_hunter").first()

        self.db.add(
            UserAchievement(
                user_id=alex.id,
                achievement_id=first_lesson.id,
                earned_at=now,
            )
        )
        self.db.add(
            UserAchievement(
                user_id=alex.id,
                achievement_id=streak_starter.id,
                earned_at=now,
            )
        )
        self.db.add(
            UserAchievement(
                user_id=alex.id,
                achievement_id=xp_hunter.id,
                earned_at=now,
            )
        )
