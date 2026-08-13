from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.course import CoursePathResponse
from app.services.course_service import CourseService

router = APIRouter(prefix="/course", tags=["course"])


@router.get("/path", response_model=CoursePathResponse)
def read_path(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CourseService(db)
    return service.get_path(current_user)
