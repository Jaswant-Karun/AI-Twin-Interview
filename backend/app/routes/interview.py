from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import schemas, models
from app.services.interview_service import InterviewService

router = APIRouter()
interview_service = InterviewService()

@router.post("/start", response_model=schemas.InterviewResponse)
async def start_interview(interview: schemas.InterviewCreate, db: Session = Depends(get_db)):
    """Start a new interview session"""
    try:
        new_interview = interview_service.create_interview(db, interview)
        return new_interview
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{interview_id}")
async def get_interview(interview_id: int, db: Session = Depends(get_db)):
    """Get interview details"""
    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

@router.get("/{interview_id}/questions")
async def get_interview_questions(interview_id: int, db: Session = Depends(get_db)):
    """Get all questions for an interview"""
    questions = db.query(models.Question).filter(
        models.Question.interview_id == interview_id
    ).order_by(models.Question.order).all()
    return questions

@router.post("/{interview_id}/end")
async def end_interview(interview_id: int, db: Session = Depends(get_db)):
    """End interview and generate results"""
    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    interview.status = "completed"
    db.commit()
    return {"message": "Interview ended", "interview_id": interview_id}
