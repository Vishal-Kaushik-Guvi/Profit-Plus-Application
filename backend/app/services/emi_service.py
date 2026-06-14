from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.emipayment import Emi, EmiPayment
from app.schemas.emi import EmiCreateRequest, EmiPaymentCreateRequest
from app.models.user import User

def create_emi(request: EmiCreateRequest, current_user: User, db: Session) -> Emi:
    new_emi = Emi(**request.model_dump())
    db.add(new_emi)
    db.commit()
    db.refresh(new_emi)
    return new_emi

def get_emis_by_business(business_id: str, current_user: User, db: Session):
    return db.query(Emi).filter(Emi.business_id == business_id).all()

def get_emi_by_id(emi_id: str, current_user: User, db: Session) -> Emi:
    emi = db.query(Emi).filter(Emi.id == emi_id).first()
    if not emi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EMI not found")
    return emi

def create_emi_payment(request: EmiPaymentCreateRequest, current_user: User, db: Session) -> EmiPayment:
    emi = get_emi_by_id(str(request.emi_id), current_user, db)
    
    payment = EmiPayment(**request.model_dump())
    db.add(payment)
    
    # Update EMI tracking
    emi.amount_paid += request.amount
    emi.remaining_balance -= request.amount
    emi.months_completed += 1
    
    db.commit()
    db.refresh(payment)
    db.refresh(emi)
    return payment
