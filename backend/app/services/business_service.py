from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business import Business, SubType
from app.models.user import User
from app.schemas.business import BusinessCreateRequest, BusinessUpdateRequest
import uuid

def create_business(
    request: BusinessCreateRequest,
    current_user: User,
    db: Session
) -> Business:
    """
    Creates a new business for the logged in user.
    Like @Service method in Spring Boot.
    """

    # Check if user already has a business with same name
    existing = db.query(Business).filter(
        Business.owner_id == current_user.id,
        Business.business_name == request.business_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a business with this name"
        )

    # Check referral code if provided
    referred_by_user_id = None
    if request.referred_by_code:
        referrer = db.query(User).filter(
            User.referral_code == request.referred_by_code
        ).first()
        if referrer:
            referred_by_user_id = referrer.id

    # Create new business
    business = Business(
        id=uuid.uuid4(),
        owner_id=current_user.id,
        business_name=request.business_name,
        phone=request.phone,
        email=request.email,
        address=request.address,
        city=request.city,
        pincode=request.pincode,
        state=request.state,
        country=request.country,
        gst=request.gst,
        bank_name=request.bank_name,
        account_number=request.account_number,
        ifsc_code=request.ifsc_code,
        branch_name=request.branch_name,
        referred_by_code=request.referred_by_code,
        referred_by_user_id=referred_by_user_id,
        subscription_type=SubType.FREE  # always starts FREE
    )

    db.add(business)
    db.commit()
    db.refresh(business)

    return business


def get_my_businesses(current_user: User, db: Session):
    """Get all businesses owned by current user"""
    return db.query(Business).filter(
        Business.owner_id == current_user.id
    ).all()


def get_business_by_id(business_id: str, current_user: User, db: Session):
    """Get a single business — must belong to current user"""
    business = db.query(Business).filter(
        Business.id == business_id,
        Business.owner_id == current_user.id
    ).first()

    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )

    return business


def update_business(
    business_id: str,
    request: BusinessUpdateRequest,
    current_user: User,
    db: Session
) -> Business:
    """Update business details"""
    business = get_business_by_id(business_id, current_user, db)

    # Only update fields that were actually sent
    # In Java → BeanUtils.copyProperties() with null ignore
    update_data = request.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(business, field, value)

    db.commit()
    db.refresh(business)

    return business


def delete_business(business_id: str, current_user: User, db: Session):
    """Delete a business"""
    business = get_business_by_id(business_id, current_user, db)

    db.delete(business)
    db.commit()

    return {"message": "Business deleted successfully"}