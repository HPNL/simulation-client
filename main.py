from pathlib import Path

from fastapi import FastAPI, Request
from fastapi import Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from starlette.responses import RedirectResponse

from app.controller.auth_controller import router as auth_router
from app.controller.simulation_controller import router as simulation_router
from app.controller.user_controller import router as user_router
from app.db.database import SessionLocal, get_db
from app.db.database import engine
from app.db.models import Base
from app.db.models import User

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Simulator Client Manager",
    description="This is the API documentation for Simulator Client Manager",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/swagger-redoc"
)

# Static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(user_router)
app.include_router(simulation_router)
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
async def home():
    return RedirectResponse(url="/login")


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
        username: str = Form(...),
        password: str = Form(...),
        db: SessionLocal = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": {},  # request باید در اینجا به درستی ارسال شود
                "error": "Invalid credentials"  # پیغام خطا
            }
        )

    return templates.TemplateResponse(
        "dashboard.html", {"request": {}, "username": user.username}
    )


@app.on_event("startup")
async def startup_event():
    """This function will be called when the app starts."""
    initialize_database()


def initialize_database():
    Base.metadata.create_all(bind=engine)
