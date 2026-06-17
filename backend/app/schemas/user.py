from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional

# ── Request Schemas ──────────────────────────────────────────────

class SendOtpRequest(BaseModel):
    """Send OTP via email"""
    email: EmailStr
    purpose: str = "signup"  # "signup" or "login" or "reset_password"


class SignupRequest(BaseModel):
    """Complete signup - after OTP is verified"""
    name: str
    phone: Optional[str] = None
    email: EmailStr
    password: str
    otp: str

    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("phone")
    def phone_number(cls, v):
        if v is not None and len(v) != 10:
            raise ValueError("Phone number must be 10 digits")
        return v


class LoginRequest(BaseModel):
    """Login with email + password"""
    email: EmailStr
    password: str


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str

# ── Response Schemas ─────────────────────────────────────────────

class UserResponse(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]
    is_verified: bool
    referral_code: Optional[str]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
