from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db.crud import create_user, get_user, create_container, get_containers_by_user
from app.db.database import get_db
from app.db.schemas import UserCreate, User, ContainerCreate

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


# --- Container CRUD Endpoints ---

@router.post("/users/{user_id}/containers/", tags=["Containers"])
def create_user_container(
        user_id: int, container: ContainerCreate, db: Session = Depends(get_db)
):
    """
    Create a new container for a specific user.

    - **user_id**: ID of the user who owns the container
    - **container data**: Details of the container (via request body)
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_container(db, container, user_id)


@router.get("/users/{user_id}/containers/", tags=["Containers"])
def get_user_containers(user_id: int, db: Session = Depends(get_db)):
    """
    Get all containers for a specific user.

    - **user_id**: ID of the user whose containers are being retrieved
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_containers_by_user(db, user_id)
