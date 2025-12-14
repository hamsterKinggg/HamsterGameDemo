"""
app config part
read config from env, provide init values
"""
# manage things together that may change in the future

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """app config class"""
    
    # app basic config
    APP_NAME: str = "HamsterGame"
    DEBUG: bool = True
    
    # DB config
    DATABASE_URL: str = "sqlite:///./hamster_game.db"
    
    # JWT config
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24 * 7  # Token lasts for 7 days
    
    # game config
    MAX_SAVE_SLOTS: int = 3  # max nb of saves
    
    # state range
    STAT_MIN: int = 0
    STAT_MAX: int = 100
    
    # init states
    INITIAL_STATS: dict = {
        "hunger": 80,
        "energy": 80,
        "clean": 80,
        "mood": 80,
        "affection": 0
    }
    
    class Config:
        # read environmental varibles from .env file
        env_file = ".env"
        env_file_encoding = "utf-8"


# create global config
settings = Settings()
