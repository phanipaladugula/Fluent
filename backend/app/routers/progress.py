from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import asyncio

from app.database import get_db, SessionLocal
from app.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserPublic
from app.schemas.lesson import LessonPublic, AnswerRequest, AnswerResponse
from app.schemas.progress import ProfileResponse
from app.services.profile_service import LeaderboardService, ProfileService, PracticeService
from app.services.user_service import UserService
from app.events import hub, safe_broadcast_leaderboard

router = APIRouter(tags=["progress"])


@router.get("/leaderboard")
def read_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = LeaderboardService(db)
    return service.get_board(current_user)


@router.get("/leaderboard/stream")
async def stream_leaderboard(request: Request):
    queue = asyncio.Queue()
    hub.subscribe(queue)

    db = SessionLocal()
    try:
        user_service = UserService(db)
        current_user = user_service.get_default_user()
        safe_broadcast_leaderboard(db, current_user)
    finally:
        db.close()

    async def event_gen():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    text = await asyncio.wait_for(queue.get(), timeout=20)
                    yield "data: " + text + "\n\n"
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            hub.unsubscribe(queue)

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/profile", response_model=ProfileResponse)
def read_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProfileService(db)
    return service.get_profile(current_user)


@router.get("/practice", response_model=LessonPublic)
def read_practice(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PracticeService(db)
    return service.get_practice_set()


@router.post("/practice/answer", response_model=AnswerResponse)
def practice_answer(
    payload: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PracticeService(db)
    return service.submit_answer(payload.exercise_id, payload.answer, current_user.hearts)


@router.post("/practice/complete", response_model=UserPublic)
def complete_practice(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated = service.refill_one_heart(current_user)
    return service.to_public(updated)
