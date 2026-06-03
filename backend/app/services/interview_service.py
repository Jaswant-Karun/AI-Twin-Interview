from sqlalchemy.orm import Session
from app.models import models, schemas
import json
from datetime import datetime
from app.services.ai_service import AIService

class InterviewService:
    def __init__(self):
        self.ai_service = AIService()
    
    async def create_interview(self, db: Session, interview: schemas.InterviewCreate):
        """Create a new interview"""
        db_interview = models.Interview(
            user_id=interview.user_id,
            role=interview.role,
            status="in_progress"
        )
        db.add(db_interview)
        db.commit()
        db.refresh(db_interview)
        
        # Generate initial questions
        await self.generate_questions(db, db_interview.id, interview.role)
        
        return db_interview
    
    async def generate_questions(self, db: Session, interview_id: int, role: str):
        """Generate interview questions based on role"""
        questions = await self.ai_service.generate_questions(role, num_questions=5)
        
        for order, q in enumerate(questions, start=1):
            db_question = models.Question(
                interview_id=interview_id,
                question_text=q["text"],
                category=q.get("category", "technical"),
                order=order
            )
            db.add(db_question)
        
        db.commit()
