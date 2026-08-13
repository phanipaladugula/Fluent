from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserPublic
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
def read_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.to_public(current_user)


@router.post("/me/simulate-day", response_model=UserPublic)
def simulate_day(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated = service.simulate_day(current_user)
    return service.to_public(updated)


@router.post("/me/refill-hearts", response_model=UserPublic)
def refill_hearts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    updated = service.refill_all_hearts(current_user)
    return service.to_public(updated)
