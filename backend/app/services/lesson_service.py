from datetime import datetime
import random

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.course import Lesson, Exercise
from app.models.progress import UserSkillProgress, UserLessonCompletion
from app.schemas.lesson import (
    LessonPublic,
    ExercisePublic,
    OptionPublic,
    AnswerResponse,
    LessonStartResponse,
    LessonCompleteResponse,
)
from app.checkers.factory import ExerciseCheckerFactory
from app.services.user_service import UserService
from app.services.gamification_service import GamificationService
from app.services.achievement_service import AchievementService


class LessonService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.gamification = GamificationService(db)
        self.achievements = AchievementService(db)
        self.checker_factory = ExerciseCheckerFactory()

    def get_lesson(self, lesson_id: int) -> LessonPublic:
        lesson = self._get_lesson_or_404(lesson_id)
        exercise_items = []
        for exercise in lesson.exercises:
            option_items = self._public_options(exercise)
            exercise_items.append(
                ExercisePublic(
                    id=exercise.id,
                    type=exercise.type,
                    prompt=exercise.prompt,
                    order_index=exercise.order_index,
                    options=option_items,
                )
            )
        return LessonPublic(
            id=lesson.id,
            skill_id=lesson.skill_id,
            title=lesson.title,
            xp_reward=lesson.xp_reward,
            exercises=exercise_items,
        )

    def _public_options(self, exercise):
        option_items = []
        for option in exercise.options:
            option_items.append(
                OptionPublic(
                    id=option.id,
                    text=option.text,
                    side=option.side,
                )
            )
        if exercise.type == "multiple_choice" or exercise.type == "fill_blank":
            random.shuffle(option_items)
        if exercise.type == "translate":
            random.shuffle(option_items)
        return option_items

    def start_lesson(self, user: User, lesson_id: int) -> LessonStartResponse:
        self.user_service.regenerate_hearts(user)
        lesson = self._get_lesson_or_404(lesson_id)
        progress = self._get_skill_progress(user.id, lesson.skill_id)

        if progress is None or not progress.is_unlocked:
            self.db.commit()
            return LessonStartResponse(
                lesson_id=lesson_id,
                hearts=user.hearts,
                can_start=False,
                message="This skill is still locked.",
            )

        if user.hearts <= 0:
            self.db.commit()
            return LessonStartResponse(
                lesson_id=lesson_id,
                hearts=user.hearts,
                can_start=False,
                message="You are out of hearts.",
            )

        self.db.commit()
        return LessonStartResponse(
            lesson_id=lesson_id,
            hearts=user.hearts,
            can_start=True,
            message="Lesson started.",
        )

    def submit_answer(self, user: User, lesson_id: int, exercise_id: int, answer: str) -> AnswerResponse:
        self.user_service.regenerate_hearts(user)
        lesson = self._get_lesson_or_404(lesson_id)
        progress = self._get_skill_progress(user.id, lesson.skill_id)
        if progress is None or not progress.is_unlocked:
            raise HTTPException(status_code=403, detail="This skill is still locked.")

        if user.hearts <= 0:
            self.db.commit()
            return AnswerResponse(
                is_correct=False,
                correct_answer="",
                hearts=user.hearts,
                out_of_hearts=True,
            )

        exercise = (
            self.db.query(Exercise)
            .filter(Exercise.id == exercise_id, Exercise.lesson_id == lesson_id)
            .first()
        )
        if exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found.")

        checker = self.checker_factory.get_checker(exercise.type)
        is_correct = checker.check(exercise, answer)

        if not is_correct:
            self.user_service.lose_heart(user)

        out_of_hearts = False
        if user.hearts <= 0:
            out_of_hearts = True

        self.db.commit()
        self.db.refresh(user)
        return AnswerResponse(
            is_correct=is_correct,
            correct_answer=exercise.correct_answer,
            hearts=user.hearts,
            out_of_hearts=out_of_hearts,
        )

    def complete_lesson(self, user: User, lesson_id: int, hearts_lost: int) -> LessonCompleteResponse:
        lesson = self._get_lesson_or_404(lesson_id)
        progress = self._get_skill_progress(user.id, lesson.skill_id)
        if progress is None or not progress.is_unlocked:
            raise HTTPException(status_code=403, detail="This skill is still locked.")

        if hearts_lost < 0:
            hearts_lost = 0
        if hearts_lost > user.max_hearts:
            hearts_lost = user.max_hearts

        xp_earned = self.gamification.apply_lesson_rewards(user, lesson, hearts_lost, progress)
        completion = UserLessonCompletion(
            user_id=user.id,
            lesson_id=lesson.id,
            completed_at=datetime.utcnow(),
            xp_earned=xp_earned,
        )
        self.db.add(completion)
        new_titles = self.achievements.evaluate_after_lesson(user, hearts_lost, lesson.skill)

        self.db.commit()
        self.db.refresh(user)
        self.db.refresh(progress)

        return LessonCompleteResponse(
            xp_earned=xp_earned,
            total_xp=user.total_xp,
            daily_xp=user.daily_xp,
            daily_goal_xp=user.daily_goal_xp,
            streak_count=user.streak_count,
            crowns=progress.crowns,
            new_achievements=new_titles,
            hearts=user.hearts,
        )

    def complete_legendary(self, user: User, skill_id: int) -> LessonCompleteResponse:
        progress = self._get_skill_progress(user.id, skill_id)
        if progress is None or not progress.is_unlocked:
            raise HTTPException(status_code=403, detail="This skill is still locked.")
        if progress.crowns < 1:
            raise HTTPException(status_code=400, detail="Finish the skill once before legendary.")

        from app.models.course import Skill

        skill = self.db.query(Skill).filter(Skill.id == skill_id).first()
        if skill is None:
            raise HTTPException(status_code=404, detail="Skill not found.")

        xp_earned = self.gamification.apply_legendary_rewards(user)
        new_titles = self.achievements.evaluate_after_lesson(user, 0, skill)
        self.db.commit()
        self.db.refresh(user)
        self.db.refresh(progress)

        return LessonCompleteResponse(
            xp_earned=xp_earned,
            total_xp=user.total_xp,
            daily_xp=user.daily_xp,
            daily_goal_xp=user.daily_goal_xp,
            streak_count=user.streak_count,
            crowns=progress.crowns,
            new_achievements=new_titles,
            hearts=user.hearts,
        )

    def _get_lesson_or_404(self, lesson_id: int) -> Lesson:
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if lesson is None:
            raise HTTPException(status_code=404, detail="Lesson not found.")
        return lesson

    def _get_skill_progress(self, user_id: int, skill_id: int):
        return (
            self.db.query(UserSkillProgress)
            .filter(
                UserSkillProgress.user_id == user_id,
                UserSkillProgress.skill_id == skill_id,
            )
            .first()
        )
