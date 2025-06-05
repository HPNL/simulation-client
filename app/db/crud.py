from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password  # هش کردن رمز عبور را اضافه کنید
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
