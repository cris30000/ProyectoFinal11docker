from fastapi import APIRouter, HTTPException, status
from app.database import get_supabase
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Modelo para crear calificación
class GradeCreate(BaseModel):
    student_id: int
    period_id: int
    subject: str
    grade_value: float
    observation: Optional[str] = None

# Modelo para actualizar calificación
class GradeUpdate(BaseModel):
    grade_value: Optional[float] = None
    observation: Optional[str] = None

@router.get("/")
async def get_grades():
    """Obtener todas las calificaciones con información de estudiantes"""
    supabase = get_supabase()
    try:
        # Obtener calificaciones con datos del estudiante
        response = supabase.table("grades").select("*, users!student_id(id, username, full_name), periods(id, name)").execute()
        return {"grades": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/student/{student_id}")
async def get_grades_by_student(student_id: int):
    """Obtener calificaciones de un estudiante específico"""
    supabase = get_supabase()
    try:
        response = supabase.table("grades").select("*, periods(name)").eq("student_id", student_id).execute()
        return {"grades": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/period/{period_id}")
async def get_grades_by_period(period_id: int):
    """Obtener calificaciones de un período específico"""
    supabase = get_supabase()
    try:
        response = supabase.table("grades").select("*, users!student_id(username, full_name)").eq("period_id", period_id).execute()
        return {"grades": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{grade_id}")
async def get_grade(grade_id: int):
    """Obtener una calificación por ID"""
    supabase = get_supabase()
    try:
        response = supabase.table("grades").select("*").eq("id", grade_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Calificación no encontrada")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_grade(grade: GradeCreate):
    """Registrar una nueva calificación"""
    supabase = get_supabase()
    
    # Verificar que el estudiante existe
    student = supabase.table("users").select("*").eq("id", grade.student_id).eq("role", "student").execute()
    if not student.data:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Verificar que el período existe
    period = supabase.table("periods").select("*").eq("id", grade.period_id).execute()
    if not period.data:
        raise HTTPException(status_code=404, detail="Período no encontrado")
    
    # Verificar que la nota está en rango válido (0-100)
    if grade.grade_value < 0 or grade.grade_value > 100:
        raise HTTPException(status_code=400, detail="La calificación debe estar entre 0 y 100")
    
    # Verificar si ya existe una calificación para este estudiante, período y materia
    existing = supabase.table("grades").select("*").eq("student_id", grade.student_id).eq("period_id", grade.period_id).eq("subject", grade.subject).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Ya existe una calificación para este estudiante en esta materia y período")
    
    new_grade = {
        "student_id": grade.student_id,
        "teacher_id": 2,  # Por defecto el teacher ID=2 (puedes cambiarlo después)
        "period_id": grade.period_id,
        "subject": grade.subject,
        "grade_value": grade.grade_value,
        "observation": grade.observation
    }
    
    try:
        response = supabase.table("grades").insert(new_grade).execute()
        return {"message": "Calificación registrada exitosamente", "grade": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/{grade_id}")
async def update_grade(grade_id: int, grade: GradeUpdate):
    """Actualizar una calificación existente"""
    supabase = get_supabase()
    
    # Verificar si existe
    existing = supabase.table("grades").select("*").eq("id", grade_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    
    # Preparar datos a actualizar
    update_data = {k: v for k, v in grade.dict().items() if v is not None}
    
    # Verificar que la nota está en rango válido
    if "grade_value" in update_data:
        if update_data["grade_value"] < 0 or update_data["grade_value"] > 100:
            raise HTTPException(status_code=400, detail="La calificación debe estar entre 0 y 100")
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    try:
        response = supabase.table("grades").update(update_data).eq("id", grade_id).execute()
        return {"message": "Calificación actualizada exitosamente", "grade": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/{grade_id}")
async def delete_grade(grade_id: int):
    """Eliminar una calificación"""
    supabase = get_supabase()
    
    # Verificar si existe
    existing = supabase.table("grades").select("*").eq("id", grade_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    
    try:
        supabase.table("grades").delete().eq("id", grade_id).execute()
        return {"message": "Calificación eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")