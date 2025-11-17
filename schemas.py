"""
Database Schemas for MyCode app

Each Pydantic model corresponds to a MongoDB collection (lowercased name).
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Appointment(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    service: str = Field(..., min_length=2, max_length=100)
    date: datetime = Field(..., description="Selected date and time in ISO format")
    notes: Optional[str] = Field(None, max_length=1000)
    status: str = Field("pending", description="pending | confirmed | cancelled")

class Message(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=150)
    message: str = Field(..., min_length=5, max_length=2000)

class Project(BaseModel):
    title: str
    description: str
    type: str = Field(..., description="web | mobile | ai | backend | devops | other")
    image_url: Optional[str] = None
    tags: List[str] = []
    url: Optional[str] = None
