"""
DB connection module
Create engine, session, and manage dependency
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator

from app.core.config import settings


# create DB engine
# check_same_thread=False is only in SQLite，allowing muti thread
engine = create_engine(
    settings.DATABASE_URL,  # this is the path of .db file
    connect_args={"check_same_thread": False},  # only in SQLite
    echo=settings.DEBUG  # print SQL languages in debug mode
)

# create session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# many SQL operations together

# create base model class（all table models inheritsmfrom it）
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    get dependency func of DB session
    for FastAPI dependencies
    
    how to use：
        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    init db: create all table
    called when starting
    """
    # import all models, register to Base.metadata
    from app.models import user, save  # noqa: F401
    
    # create tables if not exists
    Base.metadata.create_all(bind=engine)
