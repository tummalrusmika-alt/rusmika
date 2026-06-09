from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ============== User Models ==============
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: str
    full_name: str
    language: str = "en"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    language: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============== Authentication Models ==============
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

# ============== Complaint Models ==============
class ComplaintBase(BaseModel):
    title: str
    description: str
    category: str
    latitude: float
    longitude: float
    location_name: str
    language: str = "en"

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None

class ComplaintResponse(ComplaintBase):
    id: int
    user_id: int
    image_url: Optional[str]
    before_image: Optional[str]
    after_image: Optional[str]
    severity_score: float
    status: str
    is_duplicate: bool
    upvote_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ComplaintListResponse(BaseModel):
    id: int
    title: str
    category: str
    status: str
    severity_score: float
    upvote_count: int
    location_name: str
    image_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============== Upvote Models ==============
class UpvoteResponse(BaseModel):
    id: int
    complaint_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============== Department Models ==============
class DepartmentRoutingResponse(BaseModel):
    id: int
    complaint_category: str
    department_name: str
    email: str
    phone: str
    
    class Config:
        from_attributes = True

# ============== File Upload Models ==============
class FileUploadResponse(BaseModel):
    file_url: str
    file_name: str
    file_size: int
    uploaded_at: datetime

# ============== Voice Input Models ==============
class VoiceTranscriptionResponse(BaseModel):
    transcript: str
    language: str
    confidence: float
    duration: float

# ============== Statistics Models ==============
class ComplaintStats(BaseModel):
    total_complaints: int
    pending: int
    verified: int
    assigned: int
    resolved: int
    average_severity: float
    
class LocationStats(BaseModel):
    location: str
    complaint_count: int
    severity: float
    status: str
