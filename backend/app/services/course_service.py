from sqlalchemy.orm import Session

from app.models.user import User
from app.models.course import Course, Unit, Skill, Lesson
from app.models.progress import UserSkillProgress
from app.schemas.course import CoursePathResponse, UnitPathItem, SkillPathItem


class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def get_path(self, user: User) -> CoursePathResponse:
        course = self.db.query(Course).first()
        units = (
            self.db.query(Unit)
            .filter(Unit.course_id == course.id)
            .order_by(Unit.order_index)
            .all()
        )

        unit_items = []
        previous_has_crown = True

        for unit in units:
            skills = (
                self.db.query(Skill)
                .filter(Skill.unit_id == unit.id)
                .order_by(Skill.order_index)
                .all()
            )
            skill_items = []
            for skill in skills:
                should_unlock = previous_has_crown
                progress = self._get_or_create_progress(user, skill, should_unlock)
                lesson = (
                    self.db.query(Lesson)
                    .filter(Lesson.skill_id == skill.id)
                    .order_by(Lesson.order_index)
                    .first()
                )
                lesson_id = None
                if lesson is not None:
                    lesson_id = lesson.id

                is_completed = False
                if progress.crowns >= 1:
                    is_completed = True

                item = SkillPathItem(
                    id=skill.id,
                    title=skill.title,
                    description=skill.description,
                    icon=skill.icon,
                    order_index=skill.order_index,
                    max_crowns=skill.max_crowns,
                    crowns=progress.crowns,
                    is_unlocked=progress.is_unlocked,
                    is_completed=is_completed,
                    lesson_id=lesson_id,
                )
                skill_items.append(item)
                previous_has_crown = is_completed

            unit_item = UnitPathItem(
                id=unit.id,
                title=unit.title,
                description=unit.description,
                color=unit.color,
                order_index=unit.order_index,
                skills=skill_items,
            )
            unit_items.append(unit_item)

        self.db.commit()
        return CoursePathResponse(
            id=course.id,
            language_code=course.language_code,
            title=course.title,
            from_language=course.from_language,
            units=unit_items,
        )

    def _get_or_create_progress(self, user: User, skill: Skill, should_unlock: bool):
        progress = (
            self.db.query(UserSkillProgress)
            .filter(
                UserSkillProgress.user_id == user.id,
                UserSkillProgress.skill_id == skill.id,
            )
            .first()
        )
        if progress is None:
            progress = UserSkillProgress(
                user_id=user.id,
                skill_id=skill.id,
                crowns=0,
                is_unlocked=should_unlock,
            )
            self.db.add(progress)
            self.db.flush()
            return progress

        if should_unlock:
            if not progress.is_unlocked:
                progress.is_unlocked = True
                self.db.flush()
        return progress
