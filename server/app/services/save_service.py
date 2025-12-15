"""
save service - logic about saves in game
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional, Dict, Any

from app.models import Save, User
from app.core.config import settings


def get_user_saves(db: Session, user_id: int) -> List[Save]:
    """get all saves of a user"""
    saves = db.query(Save).filter(Save.user_id == user_id).order_by(Save.slot).all()
    return saves


def get_save_by_slot(db: Session, user_id: int, slot: int) -> Optional[Save]:
    """get a certain slot of a user"""
    save = db.query(Save).filter(
        Save.user_id == user_id,
        Save.slot == slot
    ).first()
    return save


def create_save(db: Session, user_id: int, slot: int, pet_name: str) -> Save:
    # usera set a name and choose a slot. states are set init values
    """
    create a new save
    
    Args:
        db: db session
        user_id: user ID
        slot: slot 1~3
        pet_name: pet name
    
    Returns:
        created new save
    
    Raises:
        HTTPException: slot occupied or #slot is over 3
    """
    # check if over 3(MAX_SAVE_SLOTS is currently 3)
    if slot < 1 or slot > settings.MAX_SAVE_SLOTS:
        raise HTTPException(
            status_code=400, 
            detail=f"Slot must be between 1 and {settings.MAX_SAVE_SLOTS}"
        )
    
    # check if slot occupied
    existing = get_save_by_slot(db, user_id, slot)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Slot {slot} is already occupied"
        )
    
    # create new
    save = Save(
        user_id=user_id,
        slot=slot,
        pet_name=pet_name
        # state_json will use init value of the beginning of game
    )
    
    db.add(save)
    db.commit() # a part of db session routine
    db.refresh(save)
    
    return save


def update_save(
    db: Session, 
    user_id: int, 
    slot: int,
    pet_name: Optional[str] = None,
    current_node: Optional[str] = None,
    state_json: Optional[Dict[str, Any]] = None
) -> Save:
    # slot cannot be changed.
    # request maybe from user who want to change name of pet
    # request may also be from client autoly when game goes on. in this case, all states are sent here as a whole
    """
    update save
    
    Args:
        db: db session
        user_id: user ID
        slot: slot 1~3
        pet_name: new name(optional)
        current_node: updated current node(optional)
        state_json: updated state(optional)
        'optional' here means requests may only update 1 of 3
    
    Returns:
        updated save
    """
    save = get_save_by_slot(db, user_id, slot)
    if not save:
        raise HTTPException(status_code=404, detail=f"Save not found in slot {slot}")
    
    # the target info to be updated
    if pet_name is not None:
        save.pet_name = pet_name
    if current_node is not None:
        save.current_node = current_node
    if state_json is not None:
        save.state_json = state_json
    
    db.commit()
    db.refresh(save)
    
    return save


def delete_save(db: Session, user_id: int, slot: int) -> bool:
    """
    delete the
    
    Returns:
        deleted successfully or not
    """
    save = get_save_by_slot(db, user_id, slot)
    if not save:
        raise HTTPException(status_code=404, detail=f"Save not found in slot {slot}")
    
    db.delete(save)
    db.commit()
    
    return True