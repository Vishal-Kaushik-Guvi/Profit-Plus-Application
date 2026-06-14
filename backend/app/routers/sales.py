from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.sales import SalesCreateRequest, SalesResponse
from app.services import sales_service

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=SalesResponse)
def create_sale(
    request: SalesCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return sales_service.create_sale(request, current_user, db)

@router.get("/business/{business_id}", response_model=List[SalesResponse])
def get_business_sales(
    business_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return sales_service.get_sales_by_business(business_id, current_user, db)

@router.get("/{sale_id}", response_model=SalesResponse)
def get_sale(
    sale_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return sales_service.get_sale_by_id(sale_id, current_user, db)
