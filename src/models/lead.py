from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class LeadStatus(str, Enum):
    DISCOVERED = "discovered"
    QUALIFIED = "qualified"
    PENDING_APPROVAL = "pending_approval"
    CONTACTED = "contacted"
    REPLIED = "replied"
    CONVERTED = "converted"
    REJECTED = "rejected"
    DISPATCH_FAILED = "dispatch_failed"
    UNQUALIFIED = "unqualified"

class OutreachChannel(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    TELEGRAM = "telegram"
    PHONE = "phone"

class AuditReport(BaseModel):
    load_time_seconds: Optional[float] = None
    ttfb_seconds: Optional[float] = None
    has_ssl: bool = True
    is_mobile_responsive: bool = True
    has_whatsapp_widget: bool = False
    has_online_booking: bool = False
    key_flaws: List[str] = Field(default_factory=list)
    quantified_loss: Optional[str] = None
    screenshot_path: Optional[str] = None
    raw_evidence_hash: Optional[str] = None
    audited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BusinessProfile(BaseModel):
    company_name: str
    business_type: str = "general"
    location: str = "Unknown"
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    has_website: bool = False
    address: Optional[str] = None
    rating: Optional[str] = None
    source: str = "manual"
    source_url: Optional[str] = None
    vertical: Optional[str] = "general"
    pain_points: List[str] = Field(default_factory=list)
    growth_goals: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OutreachDraft(BaseModel):
    whatsapp_message: Optional[str] = None
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    pain_points: List[str] = Field(default_factory=list)
    business_loss: Optional[str] = None

class Lead(BaseModel):
    id: str
    profile: BusinessProfile
    status: LeadStatus = LeadStatus.DISCOVERED
    audit: Optional[AuditReport] = None
    draft: Optional[OutreachDraft] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    budget: Optional[str] = None
    interest_level: Optional[str] = None
    summary: Optional[str] = None
    qualified: bool = False
    contacted_channels: List[OutreachChannel] = Field(default_factory=list)
    last_contacted_at: Optional[datetime] = None
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    meeting_link: Optional[str] = None
    research: Optional[Dict[str, Any]] = None
    pstack_proof: Optional[Dict[str, Any]] = None
    handoff_trace: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LeadOutput(BaseModel):
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    budget: Optional[str] = None
    interest_level: Optional[str] = None
    qualified: bool = False
    summary: Optional[str] = None
