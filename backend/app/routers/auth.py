import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import (
    SendOtpRequest,
    SignupRequest,
    LoginRequest,
    TokenResponse,
    UserResponse
)
from app.utils.email_service import send_otp_email
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


# ── Send OTP ────────────────────────────────────────────────────────

@router.post("/send-otp")
def send_otp(request: SendOtpRequest, db: Session = Depends(get_db)):
    """
    Sends OTP to email. Used for both signup and login verification.
    """
    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=5)

    existing = db.query(User).filter(User.email == request.email).first()

    if existing and existing.is_verified and request.purpose == "signup":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please log in instead."
        )

    if existing:
        existing.email_otp = otp
        existing.email_otp_expiry = otp_expiry
        user_name = existing.name or "there"
    else:
        existing = User(
            id=uuid.uuid4(),
            email=request.email,
            email_otp=otp,
            email_otp_expiry=otp_expiry,
            is_verified=False
        )
        db.add(existing)
        user_name = "there"

    db.commit()

    # Send actual email
    email_sent = send_otp_email(request.email, otp, user_name)

    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP email. Please try again."
        )

    return {"message": "OTP sent to your email successfully"}


# ── Signup ──────────────────────────────────────────────────────────

@router.post("/signup", response_model=TokenResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Complete signup with name, email, password + OTP verification.
    """
    existing = db.query(User).filter(User.email == request.email).first()

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please request an OTP first"
        )

    # Verify OTP
    if existing.email_otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.utcnow() > existing.email_otp_expiry:
        raise HTTPException(status_code=400, detail="OTP expired. Please request a new one")

    if request.phone:
        phone_owner = db.query(User).filter(User.phone == request.phone, User.id != existing.id).first()
        if phone_owner:
            raise HTTPException(status_code=400, detail="Phone number already registered")

    # Update user
    existing.name = request.name
    existing.phone = request.phone
    existing.password = hash_password(request.password)
    existing.is_verified = True
    existing.is_email_verified = True
    existing.email_otp = None
    existing.email_otp_expiry = None

    if not existing.referral_code:
        existing.referral_code = str(uuid.uuid4())[:8].upper()

    db.commit()
    db.refresh(existing)

    access_token = create_access_token(data={"sub": str(existing.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(existing.id),
            name=existing.name,
            email=existing.email,
            is_verified=existing.is_verified,
            referral_code=existing.referral_code
        )
    )


# ── Login ───────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email + password.
    """
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            is_verified=user.is_verified,
            referral_code=user.referral_code
        )
    )


# ── Get Current User ──────────────────────────────────────────────

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        is_verified=current_user.is_verified,
        referral_code=current_user.referral_code
    )
