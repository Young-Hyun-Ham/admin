# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import docs as docs_router
from .routes import chat as chat_router
from .database import lifespan_db
from .config import get_settings

settings = get_settings()

app = FastAPI(lifespan=lifespan_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # ✅ .env 반영
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs_router.router)
app.include_router(chat_router.router)

@app.get("/healthz")
def healthz():
    return {"ok": True}
