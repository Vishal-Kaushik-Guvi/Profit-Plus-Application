from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.sales import Sales, SaleItem
from app.schemas.sales import SalesCreateRequest
from app.models.user import User

def create_sale(request: SalesCreateRequest, current_user: User, db: Session) -> Sales:
    sale_data = request.model_dump(exclude={"items"})
    new_sale = Sales(**sale_data)
    db.add(new_sale)
    db.flush() # get new_sale.id
    
    for item_in in request.items:
        sale_item = SaleItem(**item_in.model_dump(), sale_id=new_sale.id)
        db.add(sale_item)
        
    db.commit()
    db.refresh(new_sale)
    return new_sale

def get_sale_by_id(sale_id: str, current_user: User, db: Session) -> Sales:
    sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale

def get_sales_by_business(business_id: str, current_user: User, db: Session):
    return db.query(Sales).filter(Sales.business_id == business_id).all()
