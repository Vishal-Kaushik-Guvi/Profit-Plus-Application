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
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


# ── Send OTP (Phone or Email) ──────────────────────────────────────

@router.post("/send-otp")
def send_otp(request: SendOtpRequest, db: Session = Depends(get_db)):
    """
    Sends OTP to either phone or email - whichever the user chose.
    """
    if not request.phone and not request.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either phone or email must be provided"
        )

    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=5)

    if request.phone:
        # Check if phone already registered (for signup flow)
        existing = db.query(User).filter(User.phone == request.phone).first()
        if existing and request.purpose == "signup":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )

        if existing:
            existing.otp = otp
            existing.otp_expiry = otp_expiry
            db.commit()
        # If new user — we don't create yet, OTP is verified at signup time

        print(f"[PHONE OTP] {request.phone}: {otp}")

    else:  # email
        existing = db.query(User).filter(User.email == request.email).first()
        if existing and request.purpose == "signup":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        if existing:
            existing.email_otp = otp
            existing.email_otp_expiry = otp_expiry
            db.commit()

        print(f"[EMAIL OTP] {request.email}: {otp}")

    return {
        "message": "OTP sent successfully",
        "otp": otp  # remove in production!
    }


# ── Signup ──────────────────────────────────────────────────────────

@router.post("/signup", response_model=TokenResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Complete signup with name, phone/email, password + OTP verification.
    """
    if not request.phone and not request.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either phone or email must be provided"
        )

    # Check for existing user
    if request.phone:
        existing = db.query(User).filter(User.phone == request.phone).first()
    else:
        existing = db.query(User).filter(User.email == request.email).first()

    # ── OTP Verification ──────────────────────────────────────────
    # For brand new signups, OTP was sent but no user record exists yet
    # We need a temporary store — simplest fix: allow OTP check against
    # a freshly created (unverified) user record

    if existing:
        # User record exists (OTP was sent to existing record)
        if request.otp_method == "phone":
            if existing.otp != request.otp:
                raise HTTPException(status_code=400, detail="Invalid OTP")
            if datetime.utcnow() > existing.otp_expiry:
                raise HTTPException(status_code=400, detail="OTP expired")
        else:  # email
            if existing.email_otp != request.otp:
                raise HTTPException(status_code=400, detail="Invalid OTP")
            if datetime.utcnow() > existing.email_otp_expiry:
                raise HTTPException(status_code=400, detail="OTP expired")

        user = existing
    else:
        # Brand new user - no OTP record exists to check against
        # In this flow, /send-otp should have created a placeholder record
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please request an OTP first"
        )

    # ── Update user with signup details ─────────────────────────────
    user.name = request.name
    user.password = hash_password(request.password)
    user.is_verified = True

    if request.phone:
        user.phone = request.phone
        user.otp = None
        user.otp_expiry = None
    if request.email:
        user.email = request.email
        user.is_email_verified = True
        user.email_otp = None
        user.email_otp_expiry = None

    if not user.referral_code:
        user.referral_code = str(uuid.uuid4())[:8].upper()

    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user.id),
            name=user.name,
            phone=user.phone,
            email=user.email,
            is_verified=user.is_verified,
            referral_code=user.referral_code
        )
    )


# ── Login (Password based) ────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with phone or email + password.
    """
    # Find user by phone or email
    user = db.query(User).filter(
        (User.phone == request.identifier) | (User.email == request.identifier)
    ).first()

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
            phone=user.phone,
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
        phone=current_user.phone,
        email=current_user.email,
        is_verified=current_user.is_verified,
        referral_code=current_user.referral_code
    )