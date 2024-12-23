from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.namespace_apis import router as namespace_router
from app.pod_apis import router as pod_router
from app.container_apis import router as container_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pods", response_class=HTMLResponse)
def get_pods_page(request: Request, namespace: str):
    return templates.TemplateResponse("pods.html", {"request": request, "namespace": namespace})


@app.get("/containers", response_class=HTMLResponse)
def get_containers_page(request: Request, namespace: str, pod: str):
    return templates.TemplateResponse("containers.html", {"request": request, "namespace": namespace, "pod": pod})
