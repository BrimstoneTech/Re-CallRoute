from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    PERSONNEL = "personnel"

class PersonnelStatus(enum.Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    OFFLINE = "offline"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.PERSONNEL)
    is_active = Column(Boolean, default=True)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # e.g., "HR", "Support", "Manager"
    description = Column(String, nullable=True)
    
    personnel = relationship("Personnel", back_populates="role")

class Personnel(Base):
    __tablename__ = "personnel"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    extension = Column(String, unique=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    status = Column(Enum(PersonnelStatus), default=PersonnelStatus.AVAILABLE)
    ip_address = Column(String, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    role = relationship("Role", back_populates="personnel")

class CallLog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    caller_id = Column(String)
    recipient_id = Column(Integer, ForeignKey("personnel.id"))
    duration_seconds = Column(Integer, nullable=True)
    status = Column(String) # e.g., "Completed", "Missed", "Redirected"
    redirection_details = Column(String, nullable=True)

    recipient = relationship("Personnel")
