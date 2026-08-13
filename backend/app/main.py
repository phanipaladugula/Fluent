from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import config
from app.database import Base, engine, SessionLocal
from app.seed import CourseSeeder
import app.models  # noqa: F401  registers tables before create_all
from app.routers.users import router as users_router
from app.routers.course import router as course_router
from app.routers.lessons import router as lessons_router
from app.routers.progress import router as progress_router


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seeder = CourseSeeder(db)
        seeder.run()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(application: FastAPI):
    seed_database()
    yield


def create_app() -> FastAPI:
    application = FastAPI(title=config.APP_NAME, lifespan=lifespan)

    origins = config.CORS_ORIGINS
    if len(origins) == 1 and origins[0] == "*":
        origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(users_router, prefix="/api")
    application.include_router(course_router, prefix="/api")
    application.include_router(lessons_router, prefix="/api")
    application.include_router(progress_router, prefix="/api")

    @application.get("/api/health")
    def health():
        return {"status": "ok"}

    return application


app = create_app()
