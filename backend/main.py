from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.database import get_supabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando API")
    try:
        supabase = get_supabase()
        response = supabase.table("users").select("count", count="exact").execute()
        logger.info(f"✅ Conectado a Supabase - Usuarios: {response.count}")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    yield
    logger.info("🛑 Cerrando")

app = FastAPI(title="University System", lifespan=lifespan)

# CORS - Amplio para pruebas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API funcionando", "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

from app.routers import users, auth, periods, grades
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(periods.router, prefix="/api/periods", tags=["Periods"])
app.include_router(grades.router, prefix="/api/grades", tags=["Grades"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)