from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserPublic(BaseModel):
    id: int
    username: str
    display_name: str
    total_xp: int
    gems: int
    hearts: int
    max_hearts: int
    streak_count: int
    last_activity_date: Optional[date]
    daily_xp: int
    daily_goal_xp: int
    seconds_to_next_heart: int = 0

    class Config:
        from_attributes = True
