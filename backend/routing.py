from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, database, schemas

router = APIRouter(prefix="/routing", tags=["call-routing"])

def analyze_intent(text: str) -> str:
    """
    Very basic keyword-based intent analysis. 
    In a real-world scenario, this would use an NLP engine.
    """
    text = text.lower()
    if "hr" in text or "human resources" in text or "payroll" in text:
        return "HR"
    if "support" in text or "technical" in text or "help" in text:
        return "Support"
    if "manager" in text or "boss" in text or "admin" in text:
        return "Manager"
    return "Default"

@router.get("/route-call", response_model=schemas.Personnel)
def get_route(intent_text: str, db: Session = Depends(database.get_db)):
    """
    Analyzes intent and finds the best available personnel.
    """
    role_name = analyze_intent(intent_text)
    
    # 1. Try to find an available person in the matched role
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if role:
        personnel = db.query(models.Personnel).filter(
            models.Personnel.role_id == role.id,
            models.Personnel.status == models.PersonnelStatus.AVAILABLE
        ).first()
        if personnel:
            return personnel

    # 2. Fallback: Find any available person in the "Default" role
    default_role = db.query(models.Role).filter(models.Role.name == "Default").first()
    if default_role:
        personnel = db.query(models.Personnel).filter(
            models.Personnel.role_id == default_role.id,
            models.Personnel.status == models.PersonnelStatus.AVAILABLE
        ).first()
        if personnel:
            return personnel

    # 3. Final Fallback: Return first available person regardless of role
    personnel = db.query(models.Personnel).filter(
        models.Personnel.status == models.PersonnelStatus.AVAILABLE
    ).first()
    
    if not personnel:
        raise HTTPException(status_code=404, detail="No available personnel found")
    
    return personnel

@router.post("/logs", response_model=schemas.CallLog)
def create_call_log(log: schemas.CallLogBase, db: Session = Depends(database.get_db)):
    new_log = models.CallLog(**log.model_dump())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/logs", response_model=List[schemas.CallLog])
def get_call_logs(db: Session = Depends(database.get_db)):
    return db.query(models.CallLog).all()
