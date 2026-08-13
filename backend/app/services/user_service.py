from datetime import datetime, date, timedelta

from sqlalchemy.orm import Session

from app.config import config
from app.models.user import User
from app.schemas.user import UserPublic


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_default_user(self) -> User:
        user = self.db.query(User).filter(User.id == config.DEFAULT_USER_ID).first()
        if user is None:
            raise ValueError("Default user is missing. Seed the database.")
        self.regenerate_hearts(user)
        self._reset_daily_xp_if_needed(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def regenerate_hearts(self, user: User):
        if user.hearts >= user.max_hearts:
            return
        if user.last_heart_at is None:
            user.last_heart_at = datetime.utcnow()
            return

        now = datetime.utcnow()
        elapsed = now - user.last_heart_at
        minutes_passed = elapsed.total_seconds() / 60.0
        gained = int(minutes_passed // config.HEART_REGEN_MINUTES)
        if gained <= 0:
            return

        new_hearts = user.hearts + gained
        if new_hearts > user.max_hearts:
            new_hearts = user.max_hearts
        user.hearts = new_hearts

        minutes_used = gained * config.HEART_REGEN_MINUTES
        user.last_heart_at = user.last_heart_at + timedelta(minutes=minutes_used)
        if user.hearts >= user.max_hearts:
            user.last_heart_at = now

    def lose_heart(self, user: User):
        if user.hearts <= 0:
            return
        if user.hearts == user.max_hearts:
            user.last_heart_at = datetime.utcnow()
        user.hearts = user.hearts - 1

    def refill_one_heart(self, user: User) -> User:
        if user.hearts < user.max_hearts:
            user.hearts = user.hearts + config.PRACTICE_HEART_REWARD
            if user.hearts > user.max_hearts:
                user.hearts = user.max_hearts
        if user.hearts >= user.max_hearts:
            user.last_heart_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def refill_all_hearts(self, user: User) -> User:
        user.hearts = user.max_hearts
        user.last_heart_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def simulate_day(self, user: User) -> User:
        today = date.today()
        if user.last_activity_date is None:
            user.last_activity_date = today - timedelta(days=1)
        else:
            user.last_activity_date = user.last_activity_date - timedelta(days=1)
        user.daily_xp = 0
        user.last_xp_date = user.last_activity_date
        self.db.commit()
        self.db.refresh(user)
        return user

    def _reset_daily_xp_if_needed(self, user: User):
        today = date.today()
        if user.last_xp_date != today:
            user.daily_xp = 0
            user.last_xp_date = today

    def seconds_until_next_heart(self, user: User) -> int:
        if user.hearts >= user.max_hearts:
            return 0
        if user.last_heart_at is None:
            return config.HEART_REGEN_MINUTES * 60
        elapsed = (datetime.utcnow() - user.last_heart_at).total_seconds()
        remain = (config.HEART_REGEN_MINUTES * 60) - elapsed
        if remain < 0:
            return 0
        return int(remain)

    def to_public(self, user: User) -> UserPublic:
        return UserPublic(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            total_xp=user.total_xp,
            gems=user.gems,
            hearts=user.hearts,
            max_hearts=user.max_hearts,
            streak_count=user.streak_count,
            last_activity_date=user.last_activity_date,
            daily_xp=user.daily_xp,
            daily_goal_xp=user.daily_goal_xp,
            seconds_to_next_heart=self.seconds_until_next_heart(user),
        )
