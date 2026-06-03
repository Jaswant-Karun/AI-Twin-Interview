from sqlalchemy.orm import Session
from app.models import models
import json
from app.services.ai_service import AIService

class EvaluationService:
    def __init__(self):
        self.ai_service = AIService()
    
    async def evaluate_answer(self, interview_id: int, question_id: int, answer_text: str, db: Session):
        """Evaluate user's answer"""
        # Get question details
        question = db.query(models.Question).filter(
            models.Question.id == question_id
        ).first()
        interview = db.query(models.Interview).filter(
            models.Interview.id == interview_id
        ).first()

        role = interview.role if interview else "interview candidate"
        ai_result = await self.ai_service.evaluate_answer(
            question.question_text if question else "",
            answer_text,
            role,
        )
        
        evaluation = models.Evaluation(
            interview_id=interview_id,
            question_id=question_id,
            answer_id=None,
            technical_score=ai_result["technical_score"],
            communication_score=ai_result["communication_score"],
            confidence_score=ai_result["confidence_score"],
            overall_score=ai_result["overall_score"],
            feedback=ai_result["feedback"]
        )
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        return evaluation
    
    def generate_interview_summary(self, db: Session, interview_id: int):
        """Generate interview summary with strengths, weaknesses, and improvements"""
        # Get all evaluations for interview
        evaluations = db.query(models.Evaluation).filter(
            models.Evaluation.interview_id == interview_id
        ).all()
        
        # Calculate overall score
        overall_score = sum(e.overall_score for e in evaluations) / len(evaluations) if evaluations else 0
        
        # Generate summary
        result = models.InterviewResult(
            interview_id=interview_id,
            overall_score=overall_score,
            strengths=json.dumps(["Communication", "Problem-solving"]),
            weaknesses=json.dumps(["Technical depth", "Time management"]),
            improvement_roadmap=json.dumps({
                "week_1": "Focus on system design",
                "week_2": "Practice coding interviews"
            })
        )
        db.add(result)
        db.commit()
        return result
