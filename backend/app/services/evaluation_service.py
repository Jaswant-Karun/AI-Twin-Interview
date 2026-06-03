from sqlalchemy.orm import Session
from app.models import models
import json

class EvaluationService:
    
    async def evaluate_answer(self, interview_id: int, question_id: int, answer_text: str, db: Session):
        """Evaluate user's answer"""
        # Get question details
        question = db.query(models.Question).filter(
            models.Question.id == question_id
        ).first()
        
        # Placeholder scores - integrate with AI service
        evaluation = models.Evaluation(
            interview_id=interview_id,
            question_id=question_id,
            answer_id=None,
            technical_score=75.0,
            communication_score=80.0,
            confidence_score=85.0,
            overall_score=80.0,
            feedback="Good response with clear explanation."
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
