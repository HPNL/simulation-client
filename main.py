from pathlib import Path

from fastapi import FastAPI, Request
from fastapi import Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from starlette.responses import RedirectResponse, Response

from app.container_apis import router as container_router
from app.controller.simulation_controller import router as simulation_router
from app.controller.user_controller import router as user_router
from app.db.database import SessionLocal, get_db
from app.db.database import engine
from app.db.models import Base
from app.db.models import User, Container
from app.namespace_apis import router as namespace_router
from app.pod_apis import router as pod_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Kuber-Based Simulator Manager",
    description="This is the API documentation for Simulator Manager",
    version="1.0.0",
    docs_url="/swagger-ui",
    redoc_url="/swagger-redoc"
)

# Static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(user_router)
app.include_router(namespace_router)
app.include_router(pod_router)
app.include_router(container_router)
app.include_router(simulation_router)


@app.get("/", response_class=HTMLResponse)
async def home():
    return RedirectResponse(url="/login")


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})


@app.post("/register")
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


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/logout")
async def logout(request: Request, response: Response):
    response.delete_cookie("access_token")
    return RedirectResponse(url="/login")


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

    # دریافت کانتینرهای کاربر
    containers = db.query(Container).filter(Container.user_id == user.id).all()
    return templates.TemplateResponse(
        "dashboard.html", {"request": {}, "username": user.username, "containers": containers}
    )


@app.on_event("startup")
async def startup_event():
    """This function will be called when the app starts."""
    initialize_database()


def initialize_database():
    # ایجاد جداول در صورت عدم وجود
    Base.metadata.create_all(bind=engine)
