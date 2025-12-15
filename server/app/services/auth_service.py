"""
auth service - login
"""

from datetime import datetime
from sqlalchemy.orm import Session

from app.models import User
from app.core.security import create_access_token


def login_or_register(db: Session, device_id: str) -> dict: 
    # this is called by api/auth.py.
    #it's a good way to seperate API and service layers.
    """
    login or register(auto)
    
    if device_id exsits, return user
    if not, create user
    
    Args:
        db: db sessions
        device_id
    
    Returns:
        {"user_id": int, "token": str, "is_new_user": bool}
    """
    # search user in db
    user = db.query(User).filter(User.device_id == device_id).first()
    
    is_new_user = False
    
    if user is None:
        # new user
        user = User(device_id=device_id)
        db.add(user)
        db.commit()
        db.refresh(user)  # refresh to get generated id
        is_new_user = True
    else:
        # user exsits, update login time 
        user.last_login_at = datetime.utcnow()
        db.commit()
    
    # generate token
    token = create_access_token(user.id)
    
    return {
        "user_id": user.id,
        "token": token,
        "is_new_user": is_new_user
    }