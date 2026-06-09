from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="user")  # user, admin, department_official
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    complaints = relationship("Complaint", back_populates="user")
    upvotes = relationship("Upvote", back_populates="user")

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String)  # pothole, garbage, streetlight, etc
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String)
    image_url = Column(String)
    before_image = Column(String)
    after_image = Column(String)
    voice_file_url = Column(String)
    severity_score = Column(Float, default=0.0)
    status = Column(String, default="pending")  # pending, verified, assigned, resolved
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = Column(Integer, ForeignKey("complaints.id"), nullable=True)
    assigned_to = Column(String)  # department
    upvote_count = Column(Integer, default=0)
    verification_date = Column(DateTime, nullable=True)
    resolved_date = Column(DateTime, nullable=True)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="complaints")
    upvotes = relationship("Upvote", back_populates="complaint")

class Upvote(Base):
    __tablename__ = "upvotes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="upvotes")
    complaint = relationship("Complaint", back_populates="upvotes")

class DepartmentRouting(Base):
    __tablename__ = "department_routing"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_category = Column(String, index=True)
    department_name = Column(String)
    email = Column(String)
    phone = Column(String)
    jurisdiction_area = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class NotificationLog(Base):
    __tablename__ = "notification_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    email_sent_to = Column(String)
    subject = Column(String)
    status = Column(String)  # sent, failed
    error_message = Column(String, nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)

# Create tables
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
Base.metadata.create_all(bind=engine)
