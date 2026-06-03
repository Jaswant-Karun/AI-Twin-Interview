import asyncio
from app.database.db import SessionLocal, init_db
from app.models import schemas
from app.services.interview_service import InterviewService
from app.services.evaluation_service import EvaluationService

async def run_demo():
    init_db()
    db = SessionLocal()
    interview_service = InterviewService()
    evaluation_service = EvaluationService()

    # Create interview
    interview_payload = schemas.InterviewCreate(user_id=1, role="Software Engineer")
    interview = await interview_service.create_interview(db, interview_payload)
    print("Created interview:", interview.id, interview.role)

    # Fetch questions
    questions = db.query(__import__('app').models.models.Question).filter(
        __import__('app').models.models.Question.interview_id == interview.id
    ).order_by(__import__('app').models.models.Question.order).all()
    print("Questions:")
    for q in questions:
        print(q.id, q.question_text)

    # Post an answer to first question
    if questions:
        q = questions[0]
        answer_text = "I have 5 years experience building scalable web services using Python and SQLAlchemy."
        # Save answer
        Answer = __import__('app').models.models.Answer
        new_answer = Answer(question_id=q.id, interview_id=interview.id, answer_text=answer_text)
        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)

        # Evaluate
        evaluation = await evaluation_service.evaluate_answer(interview.id, q.id, answer_text, db)
        print("Evaluation:", evaluation.technical_score, evaluation.communication_score, evaluation.overall_score)

    db.close()

if __name__ == "__main__":
    asyncio.run(run_demo())
