"""
应用配置模块
从环境变量读取配置，提供默认值
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    APP_NAME: str = "HamsterGame"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./hamster_game.db"
    
    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24 * 7  # Token 有效期：7天
    
    # 游戏配置
    MAX_SAVE_SLOTS: int = 3  # 最大存档槽位数
    
    # 状态值范围
    STAT_MIN: int = 0
    STAT_MAX: int = 100
    
    # 初始状态值
    INITIAL_STATS: dict = {
        "hunger": 80,
        "energy": 80,
        "clean": 80,
        "mood": 80,
        "affection": 0
    }
    
    class Config:
        # 从 .env 文件读取环境变量
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings()
