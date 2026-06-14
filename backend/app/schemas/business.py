from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SubType(str, Enum):
    PRO = "PRO"
    PLUS = "PLUS"
    FREE = "FREE"
    NONE = "NONE"

# ── Request Schemas ─────────────────────────────────────────────────

class BusinessCreateRequest(BaseModel):
    """What client sends to register a new business"""
    business_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    # GST
    gst: Optional[str] = None

    # Bank Details                        
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    branch_name: Optional[str] = None

    # Referral
    referred_by_code: Optional[str] = None

class BusinessUpdateRequest(BaseModel):
    """What client sends to update business info"""
    business_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    gst: Optional[str] = None
    logo_url: Optional[str] = None

    # Bank Details
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    branch_name: Optional[str] = None

# ── Response Schemas ────────────────────────────────────────────────

class BusinessResponse(BaseModel):
    """What server sends back"""
    id: str
    business_name: str
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    gst: Optional[str]
    gst_verified: bool
    subscription_type: str
    logo_url: Optional[str]
    bank_name: Optional[str]
    account_number: Optional[str]
    ifsc_code: Optional[str]
    branch_name: Optional[str]
    owner_id: str

    class Config:
        from_attributes = True