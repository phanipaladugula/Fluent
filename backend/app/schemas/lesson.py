from typing import List, Optional

from pydantic import BaseModel


class OptionPublic(BaseModel):
    id: int
    text: str
    side: Optional[str]


class ExercisePublic(BaseModel):
    id: int
    type: str
    prompt: str
    order_index: int
    options: List[OptionPublic]


class LessonPublic(BaseModel):
    id: int
    skill_id: int
    title: str
    xp_reward: int
    exercises: List[ExercisePublic]


class AnswerRequest(BaseModel):
    exercise_id: int
    answer: str


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    hearts: int
    out_of_hearts: bool


class LessonStartResponse(BaseModel):
    lesson_id: int
    hearts: int
    can_start: bool
    message: str


class LessonCompleteRequest(BaseModel):
    hearts_lost: int


class LessonCompleteResponse(BaseModel):
    xp_earned: int
    total_xp: int
    daily_xp: int
    daily_goal_xp: int
    streak_count: int
    crowns: int
    new_achievements: List[str]
    hearts: int
