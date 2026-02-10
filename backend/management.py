from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database, auth

router = APIRouter(prefix="/management", tags=["personnel-management"])

# Role Endpoints
@router.post("/roles", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to manage roles")
    db_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = models.Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.get("/roles", response_model=List[schemas.Role])
def get_roles(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Role).all()

# Personnel Endpoints
@router.post("/personnel", response_model=schemas.Personnel)
def create_personnel(personnel: schemas.PersonnelCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to manage personnel")
    db_personnel = db.query(models.Personnel).filter(models.Personnel.extension == personnel.extension).first()
    if db_personnel:
        raise HTTPException(status_code=400, detail="Extension already in use")
    new_personnel = models.Personnel(**personnel.model_dump())
    db.add(new_personnel)
    db.commit()
    db.refresh(new_personnel)
    return new_personnel

@router.get("/personnel", response_model=List[schemas.Personnel])
def list_personnel(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Personnel).all()

@router.patch("/personnel/{personnel_id}/status", response_model=schemas.Personnel)
def update_personnel_status(personnel_id: int, status: models.PersonnelStatus, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_personnel = db.query(models.Personnel).filter(models.Personnel.id == personnel_id).first()
    if not db_personnel:
        raise HTTPException(status_code=404, detail="Personnel not found")
    db_personnel.status = status
    db.commit()
    db.refresh(db_personnel)
    return db_personnel
