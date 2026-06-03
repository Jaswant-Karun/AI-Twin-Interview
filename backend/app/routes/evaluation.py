from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import schemas, models
from app.services.evaluation_service import EvaluationService

router = APIRouter()
evaluation_service = EvaluationService()

@router.post("/evaluate")
async def evaluate_answer(
    interview_id: int,
    question_id: int,
    answer: schemas.AnswerCreate,
    db: Session = Depends(get_db)
):
    """Evaluate user's answer"""
    try:
        # Store answer
        new_answer = models.Answer(**answer.dict())
        db.add(new_answer)
        db.commit()
        
        # Evaluate with AI
        evaluation = await evaluation_service.evaluate_answer(
            interview_id, question_id, answer.answer_text, db
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{interview_id}/summary")
async def get_interview_summary(interview_id: int, db: Session = Depends(get_db)):
    """Get evaluation summary for interview"""
    result = db.query(models.InterviewResult).filter(
        models.InterviewResult.interview_id == interview_id
    ).first()
    if not result:
        raise HTTPException(status_code=404, detail="No evaluation found")
    return result
