from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
async def register_user(email: str, name: str):
    """Register a new user"""
    return {"message": "User registered", "email": email}

@router.get("/{user_id}")
async def get_user(user_id: int):
    """Get user profile"""
    return {"user_id": user_id, "name": "User Name"}
