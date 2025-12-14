"""
用户表模型
存储用户/设备身份信息
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """用户表"""
    
    __tablename__ = "users"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 设备标识（唯一，客户端生成并持久化）
    device_id = Column(String(64), unique=True, nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联：一个用户可以有多个存档
    saves = relationship("Save", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, device_id={self.device_id[:8]}...)>"
