"""
savers table model
store all states and progress of saves
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.core.config import settings


class Save(Base):
    """saves"""
    
    __tablename__ = "saves"
    
    # PK
    id = Column(Integer, primary_key=True, index=True)
    
    # FK: user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # save slots（1, 2, 3...）
    slot = Column(Integer, nullable=False)
    
    # pet name
    pet_name = Column(String(32), default="hamster")
    
    # current story node ID
    current_node = Column(String(64), default="start")
    
    # game state JSON（item, storyposition ...）
    state_json = Column(JSON, default=lambda: Save.get_initial_state())
    
    # schema version (for future change)
    schema_version = Column(Integer, default=1)
    
    # timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # relation: belongs to some user
    user = relationship("User", back_populates="saves")
    
    @staticmethod
    def get_initial_state() -> dict:
        """this is the init states for a new save, for the 'state_json' colume"""
        return {
            "stats": settings.INITIAL_STATS.copy(),
            "inventory": {},
            "equipped": {
                "skin": "default"
            },
            "tasks": {},
            "flags": {}
        }
    
    def __repr__(self):
        return f"<Save(id={self.id}, user_id={self.user_id}, slot={self.slot})>"
    # this is for how to display, easier to read
