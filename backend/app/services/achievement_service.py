from datetime import datetime

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.course import Skill
from app.models.progress import UserSkillProgress
from app.models.achievement import Achievement, UserAchievement


class AchievementService:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_after_lesson(self, user: User, hearts_lost: int, skill: Skill):
        newly_earned = []

        first = self._grant_if_missing(user, "first_lesson")
        if first is not None:
            newly_earned.append(first.title)

        if user.streak_count >= 3:
            streak = self._grant_if_missing(user, "streak_starter")
            if streak is not None:
                newly_earned.append(streak.title)

        if user.total_xp >= 50:
            hunter = self._grant_if_missing(user, "xp_hunter")
            if hunter is not None:
                newly_earned.append(hunter.title)

        if hearts_lost == 0:
            perfect = self._grant_if_missing(user, "perfect_lesson")
            if perfect is not None:
                newly_earned.append(perfect.title)

        if self._is_unit_complete(user, skill.unit_id):
            finisher = self._grant_if_missing(user, "unit_finisher")
            if finisher is not None:
                newly_earned.append(finisher.title)

        return newly_earned

    def list_for_user(self, user: User):
        all_achievements = self.db.query(Achievement).order_by(Achievement.id).all()
        earned_rows = (
            self.db.query(UserAchievement)
            .filter(UserAchievement.user_id == user.id)
            .all()
        )
        earned_map = {}
        for row in earned_rows:
            earned_map[row.achievement_id] = row.earned_at

        result = []
        for achievement in all_achievements:
            earned_at = None
            earned = False
            if achievement.id in earned_map:
                earned = True
                earned_at = earned_map[achievement.id]
            result.append((achievement, earned, earned_at))
        return result

    def _grant_if_missing(self, user: User, code: str):
        achievement = self.db.query(Achievement).filter(Achievement.code == code).first()
        if achievement is None:
            return None

        existing = (
            self.db.query(UserAchievement)
            .filter(
                UserAchievement.user_id == user.id,
                UserAchievement.achievement_id == achievement.id,
            )
            .first()
        )
        if existing is not None:
            return None

        link = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id,
            earned_at=datetime.utcnow(),
        )
        self.db.add(link)
        return achievement

    def _is_unit_complete(self, user: User, unit_id: int):
        skills = self.db.query(Skill).filter(Skill.unit_id == unit_id).all()
        if len(skills) == 0:
            return False

        for skill in skills:
            progress = (
                self.db.query(UserSkillProgress)
                .filter(
                    UserSkillProgress.user_id == user.id,
                    UserSkillProgress.skill_id == skill.id,
                )
                .first()
            )
            if progress is None:
                return False
            if progress.crowns < 1:
                return False
        return True
