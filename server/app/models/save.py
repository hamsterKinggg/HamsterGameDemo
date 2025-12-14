"""
存档表模型
存储玩家的游戏进度和状态
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.core.config import settings


class Save(Base):
    """存档表"""
    
    __tablename__ = "saves"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键：关联用户
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # 存档槽位（1, 2, 3...）
    slot = Column(Integer, nullable=False)
    
    # 宠物名字
    pet_name = Column(String(32), default="小仓")
    
    # 当前剧情节点 ID
    current_node = Column(String(64), default="start")
    
    # 游戏状态 JSON（状态值、背包、任务进度等）
    state_json = Column(JSON, default=lambda: Save.get_initial_state())
    
    # 数据版本号（用于未来迁移）
    schema_version = Column(Integer, default=1)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联：存档属于某个用户
    user = relationship("User", back_populates="saves")
    
    @staticmethod
    def get_initial_state() -> dict:
        """获取初始游戏状态"""
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
