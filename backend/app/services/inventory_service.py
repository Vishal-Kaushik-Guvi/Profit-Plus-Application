from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreateRequest, InventoryUpdateRequest
from app.models.user import User

def create_inventory(request: InventoryCreateRequest, current_user: User, db: Session) -> Inventory:
    # A validation could be added to ensure the product belongs to the user
    new_inv = Inventory(**request.model_dump())
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)
    return new_inv

def get_inventory_by_id(inventory_id: str, current_user: User, db: Session) -> Inventory:
    # Check by joining with Business to ensure ownership, but here we assume user has access 
    # to this business's inventory. For simplicity, direct query.
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return inv

def get_inventory_by_business(business_id: str, current_user: User, db: Session):
    return db.query(Inventory).filter(Inventory.business_id == business_id).all()

def get_inventory_by_product(product_id: str, current_user: User, db: Session):
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()

def update_inventory(inventory_id: str, request: InventoryUpdateRequest, current_user: User, db: Session) -> Inventory:
    inv = get_inventory_by_id(inventory_id, current_user, db)
    
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inv, key, value)
        
    db.commit()
    db.refresh(inv)
    return inv

def delete_inventory(inventory_id: str, current_user: User, db: Session):
    inv = get_inventory_by_id(inventory_id, current_user, db)
    db.delete(inv)
    db.commit()
    return {"message": "Inventory deleted successfully"}
