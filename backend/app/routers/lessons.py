from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.lesson import (
    LessonPublic,
    AnswerRequest,
    AnswerResponse,
    LessonStartResponse,
    LessonCompleteRequest,
    LessonCompleteResponse,
)
from app.services.lesson_service import LessonService
from app.events import safe_broadcast_leaderboard

router = APIRouter(tags=["lessons"])


@router.get("/lessons/{lesson_id}", response_model=LessonPublic)
def read_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LessonService(db)
    return service.get_lesson(lesson_id)


@router.post("/lessons/{lesson_id}/start", response_model=LessonStartResponse)
def start_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LessonService(db)
    return service.start_lesson(current_user, lesson_id)


@router.post("/lessons/{lesson_id}/answer", response_model=AnswerResponse)
def answer_exercise(
    lesson_id: int,
    payload: AnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LessonService(db)
    return service.submit_answer(
        current_user,
        lesson_id,
        payload.exercise_id,
        payload.answer,
    )


@router.post("/lessons/{lesson_id}/complete", response_model=LessonCompleteResponse)
def complete_lesson(
    lesson_id: int,
    payload: LessonCompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LessonService(db)
    result = service.complete_lesson(current_user, lesson_id, payload.hearts_lost)
    safe_broadcast_leaderboard(db, current_user)
    return result


@router.post("/legendary/{skill_id}/complete", response_model=LessonCompleteResponse)
def complete_legendary(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LessonService(db)
    result = service.complete_legendary(current_user, skill_id)
    safe_broadcast_leaderboard(db, current_user)
    return result
