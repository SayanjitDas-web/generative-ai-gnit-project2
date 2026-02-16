from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.routers import auth, sessions
from backend.database import Base, engine
import os

app = FastAPI(title="AI Placement Trainer Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sessions.router)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Serve other frontend files directly if requested
@app.get("/{file_path:path}")
async def serve_frontend(file_path: str):
    full_path = os.path.join("frontend", file_path)
    if os.path.exists(full_path):
        return FileResponse(full_path)
    return {"message": "Welcome to the AI Placement Trainer Platform API"}
