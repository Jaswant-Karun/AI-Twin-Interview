from sqlalchemy.orm import Session
from app.models import models, schemas
import json
from datetime import datetime

class InterviewService:
    
    def create_interview(self, db: Session, interview: schemas.InterviewCreate):
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
        self.generate_questions(db, db_interview.id, interview.role)
        
        return db_interview
    
    def generate_questions(self, db: Session, interview_id: int, role: str):
        """Generate interview questions based on role"""
        # Questions will be fetched from AI service
        questions = [
            {
                "text": f"Tell me about your experience as a {role}?",
                "category": "behavioral",
                "order": 1
            },
            {
                "text": f"What are your key strengths in {role} role?",
                "category": "behavioral",
                "order": 2
            },
            {
                "text": "Can you walk through a challenging project you worked on?",
                "category": "technical",
                "order": 3
            }
        ]
        
        for q in questions:
            db_question = models.Question(
                interview_id=interview_id,
                question_text=q["text"],
                category=q["category"],
                order=q["order"]
            )
            db.add(db_question)
        
        db.commit()
