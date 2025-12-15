"""
authentification API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import login_or_register

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    register/logi API
    
    - send device_id
    - if new device, create a new user autoly
    - return user_id and token
    """
    # note: do not care how many tokens are signed for a same user. everytime called, sign a new valid one
    result = login_or_register(db, request.device_id)
    return LoginResponse(**result)