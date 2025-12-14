"""
数据库连接管理模块
负责创建引擎、会话、以及依赖注入
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator

from app.core.config import settings


# 创建数据库引擎
# check_same_thread=False 是 SQLite 特有的，允许多线程访问
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 专用
    echo=settings.DEBUG  # DEBUG 模式下打印 SQL 语句
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建模型基类（所有表模型都继承它）
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话的依赖函数
    用于 FastAPI 的依赖注入
    
    使用方式：
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
    初始化数据库：创建所有表
    在应用启动时调用
    """
    # 导入所有模型，确保它们被注册到 Base.metadata
    from app.models import user, save  # noqa: F401
    
    # 创建所有表（如果不存在）
    Base.metadata.create_all(bind=engine)
