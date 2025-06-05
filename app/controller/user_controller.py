from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db.crud import create_user, get_user
from app.db.database import get_db
from app.db.schemas import UserCreate, User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# --- User CRUD Endpoints ---

@router.post("/users/", response_model=User, tags=["Users"])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    - **username**: Username for the user
    - **email**: Email of the user
    - **password**: Password (will be hashed)
    """
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@router.get("/users/{user_id}", response_model=User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user details by user ID.

    - **user_id**: ID of the user to retrieve
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
