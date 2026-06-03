from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from app.database.db import Base
from datetime import datetime

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    role = Column(String(100), index=True)  # Software Engineer, Data Analyst, etc.
    status = Column(String(50), default="in_progress")  # in_progress, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, index=True)
    question_text = Column(Text)
    category = Column(String(50))  # technical, behavioral, problem-solving
    order = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, index=True)
    interview_id = Column(Integer, index=True)
    answer_text = Column(Text)
    answer_audio_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, index=True)
    question_id = Column(Integer, index=True)
    answer_id = Column(Integer, index=True)
    technical_score = Column(Float)  # 0-100
    communication_score = Column(Float)  # 0-100
    confidence_score = Column(Float)  # 0-100
    overall_score = Column(Float)  # 0-100
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InterviewResult(Base):
    __tablename__ = "interview_results"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, index=True)
    overall_score = Column(Float)
    strengths = Column(Text)  # JSON
    weaknesses = Column(Text)  # JSON
    improvement_roadmap = Column(Text)  # JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
