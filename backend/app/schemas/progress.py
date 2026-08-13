from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.user import UserPublic


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    display_name: str
    username: str
    total_xp: int
    streak_count: int
    is_current_user: bool


class AchievementPublic(BaseModel):
    id: int
    code: str
    title: str
    description: str
    icon: str
    earned: bool
    earned_at: Optional[datetime]


class ProfileResponse(BaseModel):
    user: UserPublic
    completed_lessons: int
    unlocked_skills: int
    achievements: List[AchievementPublic]
