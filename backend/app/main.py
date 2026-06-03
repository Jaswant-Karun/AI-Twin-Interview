from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from app.routes import interview, evaluation, user
from app.database.db import init_db

app = FastAPI(
    title="AI Interview Twin API",
    description="AI-powered interview assistant API",
    version="1.0.0"
)

# CORS middleware
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup():
    init_db()
    print("✅ Database initialized")

# Include routers
app.include_router(interview.router, prefix="/api/interviews", tags=["interviews"])
app.include_router(evaluation.router, prefix="/api/evaluations", tags=["evaluations"])
app.include_router(user.router, prefix="/api/users", tags=["users"])

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "AI Interview Twin API is running"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Interview Twin API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
