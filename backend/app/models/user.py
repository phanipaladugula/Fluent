from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    total_xp = Column(Integer, nullable=False, default=0)
    gems = Column(Integer, nullable=False, default=0)
    hearts = Column(Integer, nullable=False, default=5)
    max_hearts = Column(Integer, nullable=False, default=5)
    last_heart_at = Column(DateTime, nullable=True)
    streak_count = Column(Integer, nullable=False, default=0)
    last_activity_date = Column(Date, nullable=True)
    daily_xp = Column(Integer, nullable=False, default=0)
    daily_goal_xp = Column(Integer, nullable=False, default=20)
    last_xp_date = Column(Date, nullable=True)

    skill_progress = relationship("UserSkillProgress", back_populates="user")
    lesson_completions = relationship("UserLessonCompletion", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    xp_events = relationship("XpEvent", back_populates="user")
