"""
security module - JWT generation and verification
"""

# important:
# JWT is not secure, just enough for MVP.
# reason is that server will not record the tokens it sent, only verifies if a token is sent by itself
# so one can use others' deviceID to apply for a new valid token.

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(user_id: int) -> str: 
    # called by auth_service.py
    # the reason it's in core: will be called by many modules
    """
    create JWT token
    
    Args:
        user_id: userID
    
    Returns:
        JWT token string
    """
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    
    payload = {
        "sub": str(user_id),  # subject: userID
        "exp": expire,         # expiration
        "iat": datetime.utcnow()  # issued at
    }
    
    token = jwt.encode( # this is encrypt part
        payload,
        settings.JWT_SECRET_KEY,  # only server holds security key
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def verify_token(token: str) -> Optional[int]:
    """
    verify JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        userID, None if verification fails
    """
    try:
        payload = jwt.decode( # decode here, so deviceID will not be sent anymore when calling other API
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        return user_id
    except JWTError:
        return None