from fastapi import APIRouter, HTTPException, status
from app.database import get_supabase
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

# Modelo para crear período
class PeriodCreate(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime

# Modelo para actualizar período
class PeriodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

@router.get("/")
async def get_periods():
    """Obtener todos los períodos académicos"""
    supabase = get_supabase()
    try:
        response = supabase.table("periods").select("*").order("start_date", desc=False).execute()
        return {"periods": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/active")
async def get_active_period():
    """Obtener el período activo actual"""
    supabase = get_supabase()
    try:
        response = supabase.table("periods").select("*").eq("is_active", True).execute()
        if not response.data:
            return {"message": "No hay período activo", "period": None}
        return {"period": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{period_id}")
async def get_period(period_id: int):
    """Obtener un período por ID"""
    supabase = get_supabase()
    try:
        response = supabase.table("periods").select("*").eq("id", period_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Período no encontrado")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_period(period: PeriodCreate):
    """Crear un nuevo período académico"""
    supabase = get_supabase()
    
    # Verificar si ya existe un período con el mismo nombre
    existing = supabase.table("periods").select("*").eq("name", period.name).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Ya existe un período con ese nombre")
    
    # Verificar que start_date sea menor que end_date
    if period.start_date >= period.end_date:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser menor a la fecha de fin")
    
    new_period = {
        "name": period.name,
        "start_date": period.start_date.isoformat(),
        "end_date": period.end_date.isoformat(),
        "is_active": False  # Por defecto no está activo
    }
    
    try:
        response = supabase.table("periods").insert(new_period).execute()
        return {"message": "Período creado exitosamente", "period": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/{period_id}")
async def update_period(period_id: int, period: PeriodUpdate):
    """Actualizar un período existente"""
    supabase = get_supabase()
    
    # Verificar si existe
    existing = supabase.table("periods").select("*").eq("id", period_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Período no encontrado")
    
    # Preparar datos a actualizar
    update_data = {k: v for k, v in period.dict().items() if v is not None}
    
    # Convertir fechas a ISO si están presentes
    if "start_date" in update_data:
        update_data["start_date"] = update_data["start_date"].isoformat()
    if "end_date" in update_data:
        update_data["end_date"] = update_data["end_date"].isoformat()
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    try:
        response = supabase.table("periods").update(update_data).eq("id", period_id).execute()
        return {"message": "Período actualizado exitosamente", "period": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/{period_id}")
async def delete_period(period_id: int):
    """Eliminar un período"""
    supabase = get_supabase()
    
    # Verificar si existe
    existing = supabase.table("periods").select("*").eq("id", period_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Período no encontrado")
    
    # Verificar si hay calificaciones asociadas
    grades = supabase.table("grades").select("*").eq("period_id", period_id).execute()
    if grades.data:
        raise HTTPException(status_code=400, detail="No se puede eliminar el período porque tiene calificaciones asociadas")
    
    try:
        supabase.table("periods").delete().eq("id", period_id).execute()
        return {"message": "Período eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")