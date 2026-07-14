from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from app.database import Base, engine
from app.api.routes import router
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="i-Check API",
    description="Detector de IA y Plagio para documentos académicos",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix="/api/v1")

# Servir archivos estáticos (frontend)
static_dir = Path(__file__).parent.parent / "frontend"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return "<h1>i-Check API - Frontend not found</h1>"

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
