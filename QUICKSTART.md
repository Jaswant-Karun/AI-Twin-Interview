# Quick Start Guide for AI Interview Twin

## Start Building in 1 Day

### Phase 1: Setup (10 minutes)

```powershell
# 1. Copy the backend env template
Copy-Item backend/.env.example backend/.env

# 2. Add your API keys to backend/.env
# - OPENAI_API_KEY and/or GEMINI_API_KEY
# - DATABASE_URL defaults to local Postgres (adjust credentials if needed)
```

### Phase 2: Postgres Database Setup (5 minutes)

**On Windows:**

1. Install PostgreSQL 16:
   - Download from [`https://www.postgresql.org/download/windows/`](https://www.postgresql.org/download/windows/)
   - Use default port 5432
   - Set a superuser password

2. Create the database and user:

   ```powershell
   psql -U postgres
   ```

   Then in psql:

   ```sql
   CREATE USER interview_user WITH PASSWORD 'interview_password';
   CREATE DATABASE ai_interview_db OWNER interview_user;
   GRANT ALL PRIVILEGES ON DATABASE ai_interview_db TO interview_user;
   ```

3. Verify connection:

   ```powershell
   psql -h localhost -U interview_user -d ai_interview_db
   ```

4. If you used different credentials, update `backend/.env`:

   ```env
   DATABASE_URL=postgresql+psycopg://your_user:your_password@localhost:5432/your_db
   ```

### Phase 3: Backend Development (3-4 hours)

**Priority Tasks:**

1. ✅ API endpoints scaffolding (DONE)
2. 🔧 **NEXT: Implement AI integration** (ai_service.py)
   - Add OpenAI API calls for question generation
   - Add answer evaluation logic
3. 🔧 Database models (DONE)
4. 🔧 Answer evaluation endpoint
5. 🔧 Interview results aggregation

**Command to start:**

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH='.'
uvicorn app.main:app --reload
```

### Phase 4: Frontend Development (2-3 hours)

**Priority Tasks:**

1. ✅ Component structure (DONE)
2. ✅ Pages scaffolding (DONE)
3. 🔧 **NEXT: Connect to backend APIs**
4. 🔧 Test voice input functionality
5. 🔧 Polish UI/UX

**Command to start:**

```powershell
cd frontend
npm install
npm run dev
```

### AI Connectivity Check

Run this after adding keys to `backend/.env`:

```powershell
cd backend
$env:PYTHONPATH='.'
python scripts/test_connectivity.py
```

### Phase 5: Integration & Testing (1-2 hours)

1. Test end-to-end flow
2. Handle error cases
3. Optimize UI/UX
4. Prepare demo

---

## Implementation Checklist

### Backend Priority

- [ ] Implement OpenAI integration in `ai_service.py`
- [ ] Connect `generate_questions()` to API
- [ ] Connect `evaluate_answer()` to API
- [ ] Test all endpoints with Postman/curl
- [ ] Add error handling
- [ ] Add input validation

### Frontend Priority

- [ ] Connect API calls in `interviewStore.js`
- [ ] Test role selector → interview flow
- [ ] Test voice input (if time permits)
- [ ] Add loading states
- [ ] Test results display
- [ ] Mobile responsiveness check

### Demo Flow

1. Select role (SWE, DA, etc.)
2. Get first question
3. Submit answer (text or voice)
4. See evaluation & feedback
5. Move to next question
6. Get final results summary

---

## Key Implementation Notes

### For Backend

- Use `app/services/ai_service.py` for all API calls
- Keep evaluation logic in `evaluation_service.py`
- Database queries in models.py SQLAlchemy
- Return JSON responses with proper status codes

### For Frontend

- State management via `interviewStore.js` (Zustand)
- Use API URL from `process.env.NEXT_PUBLIC_API_URL`
- Handle loading & error states for judge demo
- Use toast notifications for feedback

### For Demo

- Have sample answers prepared
- Test with real API keys
- Have fallback data if APIs are down
- Time it: intro → complete 1 interview in 2 minutes max

---

## Success Criteria

✅ **Judge Demo Can:**

1. Select role
2. Answer 2-3 questions
3. See real AI evaluations
4. View final score & recommendations
5. All within 5 minutes

**This is buildable in 1 day. Focus on:**

- ✅ Core flow working
- ✅ AI integration connected
- ✅ Nice UI (Tailwind done!)
- ⚠️ Don't over-engineer, keep it simple!

---

## Useful Links

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google Gemini Docs](https://ai.google.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Next.js Docs](https://nextjs.org/docs)

Good luck! You got this!
