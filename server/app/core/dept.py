"""
generic dependency module
provide reusable dependency functions
"""

from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.core.security import verify_token
from app.models import User


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    # for other APIs(despite public ones like /health, /doc...), get to know the user who send the request
    # get user id by verifying token
    """
    get user id from headder
    
    how to use：
        @router.get("/example")
        def example(user: User = Depends(get_current_user)):
            # current user
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # Token dorm: "Bearer eyJhbGci..."
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = parts[1]
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == user_id).first()
    # search in user table
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user