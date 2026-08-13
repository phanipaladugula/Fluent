from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    language_code = Column(String, nullable=False)
    title = Column(String, nullable=False)
    from_language = Column(String, nullable=False)

    units = relationship("Unit", back_populates="course", order_by="Unit.order_index")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    color = Column(String, nullable=False)

    course = relationship("Course", back_populates="units")
    skills = relationship("Skill", back_populates="unit", order_by="Skill.order_index")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    icon = Column(String, nullable=False)
    max_crowns = Column(Integer, nullable=False, default=5)

    unit = relationship("Unit", back_populates="skills")
    lessons = relationship("Lesson", back_populates="skill", order_by="Lesson.order_index")
    progress_rows = relationship("UserSkillProgress", back_populates="skill")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    title = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    xp_reward = Column(Integer, nullable=False, default=10)

    skill = relationship("Skill", back_populates="lessons")
    exercises = relationship(
        "Exercise",
        back_populates="lesson",
        order_by="Exercise.order_index",
    )


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    type = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)

    lesson = relationship("Lesson", back_populates="exercises")
    options = relationship(
        "ExerciseOption",
        back_populates="exercise",
        order_by="ExerciseOption.order_index",
    )


class ExerciseOption(Base):
    __tablename__ = "exercise_options"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    pair_group = Column(Integer, nullable=True)
    side = Column(String, nullable=True)
    order_index = Column(Integer, nullable=False)

    exercise = relationship("Exercise", back_populates="options")
