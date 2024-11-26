from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.namespace_apis import router as namespace_router
from app.pod_apis import router as pod_router
from app.container_apis import router as container_router

app = FastAPI()

# Static files
app.mount("static", StaticFiles(directory="/static"), name="static")

# Templates
templates = Jinja2Templates(directory="/templates")

app.include_router(namespace_router)
app.include_router(pod_router)
app.include_router(container_router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
