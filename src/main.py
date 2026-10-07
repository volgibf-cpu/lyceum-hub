from fastapi import FastAPI, Request
from src.api import user, auth, pair, grade
from src.models.models import Base
from src.core.database import engine
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from src.admin import setup_admin
import os
from dotenv import load_dotenv
import base64

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500",
                   "http://localhost:8000",],
    allow_credentials=True,                   
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def create_db():
    Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(pair.router)
app.include_router(grade.router)

setup_admin(app)


SRC_DIR = Path(__file__).resolve().parent            # lyceum_hub/src
FRONTEND_DIR = SRC_DIR.parent / "frontend"           # lyceum_hub/frontend

print(f"📂 FRONTEND_DIR = {FRONTEND_DIR}")
print(f"📂 Существует?  = {FRONTEND_DIR.exists()}")

if FRONTEND_DIR.exists():
    # Статика (css, js)
    static_dir = FRONTEND_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # HTML-страницы: /app/schedule.html, /app/login.html и т.д.
    @app.get("/app/{path:path}")
    def serve_frontend(path: str):
        full = FRONTEND_DIR / path
        if full.is_file():
            return FileResponse(full)
        return {"detail": f"Файл {path} не найден"}


@app.get("/favicon.ico")
def favicon():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎓</text></svg>'''
    return Response(content=svg, media_type="image/svg+xml")


@app.middleware("http")
async def admin_basic_auth(request: Request, call_next):
    if request.url.path.startswith("/admin"):
        auth = request.headers.get("Authorization", "")

        if auth.startswith("Basic "):
            try:
                decoded = base64.b64decode(auth[6:]).decode("ascii")
                username, _, password = decoded.partition(":")

                if (username == os.getenv("ADMIN_USER")
                        and password == os.getenv("ADMIN_PASS")):
                    return await call_next(request)
            except Exception:
                pass

        return Response(
            status_code=401,
            content="Требуется авторизация",
            headers={"WWW-Authenticate": 'Basic realm="Admin"'},
        )

    return await call_next(request)