from fastapi import Form, Depends
from fastapi import Request, APIRouter
from passlib.hash import bcrypt
from starlette.responses import RedirectResponse, Response

from app.db.database import SessionLocal, get_db
from app.db.models import User

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register")
async def register(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: SessionLocal = Depends(get_db),
):
    password_hash = bcrypt.hash(password)
    user = User(username=username, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login")


@router.get("/logout")
async def logout(request: Request, response: Response):
    response.delete_cookie("access_token")
    return RedirectResponse(url="/login")
