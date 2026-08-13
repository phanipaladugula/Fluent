import os
from pathlib import Path


def backend_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_database_path() -> str:
    fluent_path = backend_root() / "data" / "fluent.db"
    lingo_data = backend_root() / "data" / "lingo.db"
    legacy_path = backend_root() / "lingo.db"
    if fluent_path.exists():
        return str(fluent_path)
    if lingo_data.exists():
        return str(lingo_data)
    if legacy_path.exists():
        return str(legacy_path)
    return str(fluent_path)


def split_csv(raw: str) -> list[str]:
    values = []
    parts = raw.split(",")
    for part in parts:
        item = part.strip()
        if item != "":
            values.append(item)
    return values


def sqlite_url(file_path: str) -> str:
    absolute = Path(file_path).expanduser().resolve()
    return "sqlite:///" + absolute.as_posix()


def load_env_file(path: Path):
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key not in os.environ:
            os.environ[key] = value


load_env_file(backend_root() / ".env")


class AppConfig:
    def __init__(self):
        self.APP_NAME = "Fluent"
        self.DATABASE_PATH = os.environ.get("DATABASE_PATH", default_database_path())
        database_url = os.environ.get("DATABASE_URL", "")
        if database_url != "":
            self.DATABASE_URL = database_url
        else:
            self.DATABASE_URL = sqlite_url(self.DATABASE_PATH)

        cors_raw = os.environ.get(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )
        self.CORS_ORIGINS = split_csv(cors_raw)

        self.DEFAULT_USER_ID = 1
        self.MAX_HEARTS = 5
        self.HEART_REGEN_MINUTES = 30
        self.LESSON_XP = 10
        self.PERFECT_BONUS_XP = 5
        self.LEGENDARY_XP = 20
        self.DAILY_GOAL_XP = 20
        self.PRACTICE_HEART_REWARD = 1


config = AppConfig()
