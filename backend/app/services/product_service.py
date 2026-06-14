from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product import Product
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest
from app.models.user import User
import uuid

def create_product(request: ProductCreateRequest, current_user: User, db: Session) -> Product:
    new_product = Product(
        **request.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_product_by_id(product_id: str, current_user: User, db: Session) -> Product:
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.owner_id == current_user.id
    ).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

def get_products_by_business(business_id: str, current_user: User, db: Session):
    products = db.query(Product).filter(
        Product.business_id == business_id,
        Product.owner_id == current_user.id
    ).all()
    return products

def update_product(product_id: str, request: ProductUpdateRequest, current_user: User, db: Session) -> Product:
    product = get_product_by_id(product_id, current_user, db)
    
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: str, current_user: User, db: Session):
    product = get_product_by_id(product_id, current_user, db)
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
