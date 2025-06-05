from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@postgres-ut:5433/simulation_client"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# ایجاد کلاس SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# پایه برای تعریف مدل‌ها
Base = declarative_base()


# Dependency برای استفاده از سشن در روت‌ها
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
