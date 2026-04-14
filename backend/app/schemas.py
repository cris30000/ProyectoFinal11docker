from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PeriodBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime

class PeriodCreate(PeriodBase):
    pass

class PeriodResponse(PeriodBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class GradeBase(BaseModel):
    student_id: int
    period_id: int
    subject: str
    grade_value: float = Field(..., ge=0, le=100)
    observation: Optional[str] = None

class GradeResponse(GradeBase):
    id: int
    teacher_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True