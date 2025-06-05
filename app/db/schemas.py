from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# --- User Models ---

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, description="Username of the user")
    email: EmailStr = Field(..., description="Email of the user")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, description="Password of the user")


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# --- API Response Models ---

class ApiResponse(BaseModel):
    """
    Generic response model for API success or error messages.
    """
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
