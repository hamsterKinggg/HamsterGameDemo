"""
save API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.deps import get_current_user
from app.core.config import settings
from app.models import User
from app.schemas.save import (
    CreateSaveRequest, 
    UpdateSaveRequest,
    SaveBrief,
    SaveDetail,
    SaveListResponse,
    CreateSaveResponse
)
from app.services import save_service

router = APIRouter()


@router.get("/list", response_model=SaveListResponse)
def get_saves(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """get all saves of a certain user by calling get_user_saves(). return list of brievies"""
    saves = save_service.get_user_saves(db, user.id)
    return SaveListResponse(
        saves=[SaveBrief.model_validate(s) for s in saves],
        max_slots=settings.MAX_SAVE_SLOTS
    )


@router.get("/{slot}", response_model=SaveDetail)
def get_save(
    slot: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """get detail of a certain slot by calling get_save_by_slot"""
    save = save_service.get_save_by_slot(db, user.id, slot)
    if not save:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Save not found in slot {slot}")
    return SaveDetail.model_validate(save)


@router.post("/create", response_model=CreateSaveResponse)
def create_save(
    request: CreateSaveRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """create a new save"""
    save = save_service.create_save(
        db=db,
        user_id=user.id,
        slot=request.slot,
        pet_name=request.pet_name
    )# init values are defined in /models/save.py
    return CreateSaveResponse(
        message="Save created successfully",
        save=SaveDetail.model_validate(save)
    )


@router.put("/{slot}", response_model=SaveDetail)
def update_save(
    slot: int,
    request: UpdateSaveRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """update a save"""
    save = save_service.update_save(
        db=db,
        user_id=user.id,
        slot=slot,
        pet_name=request.pet_name,
        current_node=request.current_node,
        state_json=request.state_json
    )
    return SaveDetail.model_validate(save)
    # model_validate(): ORM object -> pydantic, for fastAPI to transfer it to json


@router.delete("/{slot}")
def delete_save(
    slot: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """delete a seve"""
    save_service.delete_save(db, user.id, slot)
    return {"message": f"Save in slot {slot} deleted successfully"}