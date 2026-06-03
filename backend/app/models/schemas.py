from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InterviewCreate(BaseModel):
    user_id: int
    role: str  # e.g., "Software Engineer", "Data Analyst"

class InterviewResponse(BaseModel):
    id: int
    user_id: int
    role: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    interview_id: int
    question_text: str
    category: str
    order: int
    
    class Config:
        from_attributes = True

class AnswerCreate(BaseModel):
    question_id: int
    interview_id: int
    answer_text: str
    answer_audio_url: Optional[str] = None

class AnswerResponse(BaseModel):
    id: int
    question_id: int
    answer_text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class EvaluationResponse(BaseModel):
    id: int
    technical_score: float
    communication_score: float
    confidence_score: float
    overall_score: float
    feedback: str
    
    class Config:
        from_attributes = True

class InterviewResultResponse(BaseModel):
    id: int
    interview_id: int
    overall_score: float
    strengths: str
    weaknesses: str
    improvement_roadmap: str
    created_at: datetime
    
    class Config:
        from_attributes = True
