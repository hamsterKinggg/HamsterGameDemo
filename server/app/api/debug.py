"""
debug API for devaloping env
to check db tables
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import User, Save
from app.core.config import settings

router = APIRouter()


@router.get("/tables")
def list_tables():
    """display all table names"""
    return {
        "tables": ["users", "saves"],
        "warning": "Debug API - 仅开发环境使用"
    }


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    """check all users"""
    users = db.query(User).all()
    return {
        "count": len(users),
        "users": [
            {
                "id": u.id,
                "device_id": u.device_id,
                "created_at": str(u.created_at),
                "last_login_at": str(u.last_login_at)
            }
            for u in users
        ]
    }


@router.get("/saves")
def get_all_saves(db: Session = Depends(get_db)):
    """check all saves"""
    saves = db.query(Save).all()
    return {
        "count": len(saves),
        "saves": [
            {
                "id": s.id,
                "user_id": s.user_id,
                "slot": s.slot,
                "pet_name": s.pet_name,
                "current_node": s.current_node,
                "state_json": s.state_json,
                "schema_version": s.schema_version,
                "created_at": str(s.created_at),
                "updated_at": str(s.updated_at)
            }
            for s in saves
        ]
    }


@router.get("/user/{user_id}")
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    """check a single user and its saves"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    
    saves = db.query(Save).filter(Save.user_id == user_id).all()
    return {
        "user": {
            "id": user.id,
            "device_id": user.device_id,
            "created_at": str(user.created_at)
        },
        "saves": [
            {
                "slot": s.slot,
                "pet_name": s.pet_name,
                "current_node": s.current_node,
                "state_json": s.state_json
            }
            for s in saves
        ]
    }