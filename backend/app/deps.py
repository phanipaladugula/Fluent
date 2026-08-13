from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.user_service import UserService


def get_current_user(db: Session = Depends(get_db)) -> User:
    service = UserService(db)
    return service.get_default_user()
