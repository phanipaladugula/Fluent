from sqlalchemy.orm import Session
from fastapi import HTTPException
import random

from app.models.user import User
from app.models.course import Exercise
from app.models.progress import UserLessonCompletion, UserSkillProgress
from app.schemas.progress import LeaderboardEntry, ProfileResponse, AchievementPublic
from app.schemas.lesson import LessonPublic, ExercisePublic, OptionPublic, AnswerResponse
from app.services.achievement_service import AchievementService
from app.services.user_service import UserService
from app.checkers.factory import ExerciseCheckerFactory


class LeaderboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_board(self, current_user: User):
        users = self.db.query(User).order_by(User.total_xp.desc(), User.id.asc()).all()
        entries = []
        rank = 1
        for user in users:
            is_current = False
            if user.id == current_user.id:
                is_current = True
            entry = LeaderboardEntry(
                rank=rank,
                user_id=user.id,
                display_name=user.display_name,
                username=user.username,
                total_xp=user.total_xp,
                streak_count=user.streak_count,
                is_current_user=is_current,
            )
            entries.append(entry)
            rank = rank + 1
        return entries


class ProfileService:
    def __init__(self, db: Session):
        self.db = db
        self.achievements = AchievementService(db)

    def get_profile(self, user: User) -> ProfileResponse:
        completed = (
            self.db.query(UserLessonCompletion)
            .filter(UserLessonCompletion.user_id == user.id)
            .count()
        )
        unlocked = (
            self.db.query(UserSkillProgress)
            .filter(
                UserSkillProgress.user_id == user.id,
                UserSkillProgress.is_unlocked == True,
            )
            .count()
        )
        achievement_rows = self.achievements.list_for_user(user)
        achievement_items = []
        for row in achievement_rows:
            achievement = row[0]
            earned = row[1]
            earned_at = row[2]
            achievement_items.append(
                AchievementPublic(
                    id=achievement.id,
                    code=achievement.code,
                    title=achievement.title,
                    description=achievement.description,
                    icon=achievement.icon,
                    earned=earned,
                    earned_at=earned_at,
                )
            )
        return ProfileResponse(
            user=UserService(self.db).to_public(user),
            completed_lessons=completed,
            unlocked_skills=unlocked,
            achievements=achievement_items,
        )


class PracticeService:
    def __init__(self, db: Session):
        self.db = db

    def get_practice_set(self) -> LessonPublic:
        exercises = (
            self.db.query(Exercise)
            .filter(Exercise.type == "multiple_choice")
            .order_by(Exercise.id.asc())
            .limit(5)
            .all()
        )
        exercise_items = []
        for exercise in exercises:
            option_items = []
            for option in exercise.options:
                option_items.append(
                    OptionPublic(
                        id=option.id,
                        text=option.text,
                        side=option.side,
                    )
                )
            random.shuffle(option_items)
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
            id=0,
            skill_id=0,
            title="Practice",
            xp_reward=0,
            exercises=exercise_items,
        )

    def submit_answer(self, exercise_id: int, answer: str, hearts: int) -> AnswerResponse:
        exercise = self.db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found.")
        factory = ExerciseCheckerFactory()
        checker = factory.get_checker(exercise.type)
        is_correct = checker.check(exercise, answer)
        return AnswerResponse(
            is_correct=is_correct,
            correct_answer=exercise.correct_answer,
            hearts=hearts,
            out_of_hearts=False,
        )
