from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
import re

# ── Request Schemas ──────────────────────────────────────────────

class SendOtpRequest(BaseModel):
    """Send OTP via phone OR email - client chooses delivery method"""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    purpose: str = "signup"  # "signup" or "login" or "reset_password"

    @field_validator("phone")
    def validate_phone(cls, v):
        if v and not re.match(r"^\d{10}$", v):
            raise ValueError("Phone must be 10 digits")
        return v

    @field_validator("email")
    def check_one_provided(cls, v, info):
        # Either phone or email must be provided - checked in service layer
        return v


class SignupRequest(BaseModel):
    """Complete signup - after OTP is verified"""
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    otp: str
    otp_method: str  # "phone" or "email" - tells us which OTP field to check

    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class LoginRequest(BaseModel):
    """Login with phone/email + password"""
    identifier: str  # phone or email
    password: str


class VerifyOtpRequest(BaseModel):
    """Generic OTP verify - used for password reset etc"""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    otp: str


class RefreshTokenRequest(BaseModel):
    phone: str

# ── Response Schemas ─────────────────────────────────────────────

class UserResponse(BaseModel):
    id: str
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    is_verified: bool
    referral_code: Optional[str]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse