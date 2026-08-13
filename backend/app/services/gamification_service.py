from datetime import datetime, date, timedelta

from sqlalchemy.orm import Session

from app.config import config
from app.models.user import User
from app.models.course import Skill
from app.models.progress import UserSkillProgress, XpEvent


class GamificationService:
    def __init__(self, db: Session):
        self.db = db

    def apply_lesson_rewards(self, user: User, lesson, hearts_lost: int, skill_progress: UserSkillProgress) -> int:
        xp = lesson.xp_reward
        if hearts_lost == 0:
            xp = xp + config.PERFECT_BONUS_XP

        self._add_xp(user, xp, "lesson_complete")
        self.update_streak(user)
        self._add_crown(skill_progress)
        self.unlock_next_skill(user, skill_progress.skill)
        return xp

    def apply_legendary_rewards(self, user: User) -> int:
        xp = config.LEGENDARY_XP
        self._add_xp(user, xp, "legendary_complete")
        self.update_streak(user)
        return xp

    def update_streak(self, user: User):
        today = date.today()
        if user.last_activity_date is None:
            user.streak_count = 1
            user.last_activity_date = today
            return

        if user.last_activity_date == today:
            return

        yesterday = today - timedelta(days=1)
        if user.last_activity_date == yesterday:
            user.streak_count = user.streak_count + 1
            user.last_activity_date = today
            return

        user.streak_count = 1
        user.last_activity_date = today

    def _add_xp(self, user: User, amount: int, reason: str):
        today = date.today()
        if user.last_xp_date != today:
            user.daily_xp = 0
            user.last_xp_date = today
        user.daily_xp = user.daily_xp + amount
        user.total_xp = user.total_xp + amount

        event = XpEvent(
            user_id=user.id,
            amount=amount,
            reason=reason,
            created_at=datetime.utcnow(),
        )
        self.db.add(event)

    def _add_crown(self, skill_progress: UserSkillProgress):
        skill = skill_progress.skill
        if skill_progress.crowns < skill.max_crowns:
            skill_progress.crowns = skill_progress.crowns + 1

    def unlock_next_skill(self, user: User, current_skill: Skill):
        ordered_skills = self._all_skills_in_order()
        current_index = 0
        found = False
        while current_index < len(ordered_skills):
            if ordered_skills[current_index].id == current_skill.id:
                found = True
                break
            current_index = current_index + 1

        if not found:
            return
        next_index = current_index + 1
        if next_index >= len(ordered_skills):
            return

        next_skill = ordered_skills[next_index]
        progress = (
            self.db.query(UserSkillProgress)
            .filter(
                UserSkillProgress.user_id == user.id,
                UserSkillProgress.skill_id == next_skill.id,
            )
            .first()
        )
        if progress is None:
            progress = UserSkillProgress(
                user_id=user.id,
                skill_id=next_skill.id,
                crowns=0,
                is_unlocked=True,
            )
            self.db.add(progress)
            return
        progress.is_unlocked = True

    def _all_skills_in_order(self):
        from app.models.course import Unit

        units = self.db.query(Unit).order_by(Unit.order_index).all()
        result = []
        for unit in units:
            skills = (
                self.db.query(Skill)
                .filter(Skill.unit_id == unit.id)
                .order_by(Skill.order_index)
                .all()
            )
            for skill in skills:
                result.append(skill)
        return result
