import asyncio
import os
from app.services.ai_service import AIService

async def main():
    service = AIService()
    role = os.getenv('TEST_ROLE', 'Software Engineer')
    print('Testing generate_questions for role:', role)
    try:
        qs = await service.generate_questions(role, num_questions=3)
        print('Questions:', qs)
    except Exception as e:
        print('generate_questions raised:', e)

    print('\nTesting evaluate_answer')
    try:
        res = await service.evaluate_answer(
            'Describe a system you designed',
            'I designed a microservice-based order processing system with retries and idempotency.',
            role
        )
        print('Evaluation result:', res)
    except Exception as e:
        print('evaluate_answer raised:', e)

if __name__ == '__main__':
    asyncio.run(main())
