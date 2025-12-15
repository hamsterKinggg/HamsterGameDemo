"""
存档相关的数据格式定义
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


# ===== request schema =====

class CreateSaveRequest(BaseModel):
    """to create a new save"""
    slot: int  # slot 1, 2, 3
    pet_name: str


class UpdateSaveRequest(BaseModel):
    """to updete a save"""
    pet_name: Optional[str] = None  # change name(optional)
    current_node: Optional[str] = None  # update story node(optional)
    state_json: Optional[Dict[str, Any]] = None  # update states(optional)
    # 'optional' here means user may only update 1 of these 3


# ===== response schema =====

class SaveBrief(BaseModel):
    # used for displaying slot for user to choose
    """save's brief info for list"""
    id: int
    slot: int
    pet_name: str
    current_node: str
    updated_at: datetime
    
    class Config:
        from_attributes = True  # allow being trasfered from ORm object


class SaveDetail(BaseModel):
    """save details"""
    # all info storied in save table
    id: int
    slot: int
    pet_name: str
    current_node: str
    state_json: Dict[str, Any]
    schema_version: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SaveListResponse(BaseModel):
    # every element in this list is a save brief
    """save list response"""
    saves: List[SaveBrief]
    max_slots: int  # most slot


class CreateSaveResponse(BaseModel):
    """feedback for creating a save"""
    message: str
    save: SaveDetail