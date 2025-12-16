"""
generic dependency module
provide reusable dependency functions
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.core.security import verify_token
from app.models import User

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    # for other APIs(despite public ones like /health, /doc...), get to know the user who send the request
    # get user id by verifying token
    """
    get user id from headder
    
    how to use:
        @router.get("/example")
        def example(user: User = Depends(get_current_user)):
            # current user
    """
   
    # Token dorm: "Bearer eyJhbGci..."
    token = credentials.credentials
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user