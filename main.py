from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.namespace_apis import router as namespace_router
from app.pod_apis import router as pod_router
from app.controller.user_controller import router as user_router
from app.container_apis import router as container_router

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


@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/pods", response_class=HTMLResponse)
def get_pods_page(request: Request, namespace: str):
    return templates.TemplateResponse("pods.html", {"request": request, "namespace": namespace})


@app.get("/api/v1/containers", response_class=HTMLResponse)
def get_containers_page(request: Request, namespace: str, pod: str):
    return templates.TemplateResponse("containers.html", {"request": request, "namespace": namespace, "pod": pod})
