from typing import List, Optional

from pydantic import BaseModel


class SkillPathItem(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    order_index: int
    max_crowns: int
    crowns: int
    is_unlocked: bool
    is_completed: bool
    lesson_id: Optional[int]


class UnitPathItem(BaseModel):
    id: int
    title: str
    description: str
    color: str
    order_index: int
    skills: List[SkillPathItem]


class CoursePathResponse(BaseModel):
    id: int
    language_code: str
    title: str
    from_language: str
    units: List[UnitPathItem]
