from sqlalchemy.orm import Session
from app.db.models import User, Container
from app.db.schemas import UserCreate, ContainerCreate


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


def create_container(db: Session, container: ContainerCreate, user_id: int):
    new_container = Container(
        **container.dict(),
        user_id=user_id
    )
    db.add(new_container)
    db.commit()
    db.refresh(new_container)
    return new_container


def get_containers_by_user(db: Session, user_id: int):
    return db.query(Container).filter(Container.user_id == user_id).all()
