from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentUpload(BaseModel):
    filename: str
    content: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class AnalysisResultResponse(BaseModel):
    id: int
    document_id: int
    ai_percentage: float
    plagiarism_percentage: float
    analyzed_at: datetime

    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    document_id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
