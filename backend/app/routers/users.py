from fastapi import APIRouter, HTTPException
from app.database import get_supabase
from pydantic import BaseModel
from typing import Optional
import bcrypt

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str
    role: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    hashed_password: Optional[str] = None

@router.get("/")
async def get_users():
    supabase = get_supabase()
    response = supabase.table("users").select("*").execute()
    return {"users": response.data}

@router.get("/{user_id}")
async def get_user(user_id: int):
    supabase = get_supabase()
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return response.data[0]

@router.post("/")
async def create_user(user: UserCreate):
    supabase = get_supabase()
    
    # Verificar si ya existe
    existing = supabase.table("users").select("*").eq("username", user.username).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    
    existing_email = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing_email.data:
        raise HTTPException(status_code=400, detail="El email ya existe")
    
    # Hashear la contraseña
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    
    new_user = {
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "hashed_password": hashed_password.decode('utf-8'),
        "role": user.role,
        "is_active": True
    }
    
    response = supabase.table("users").insert(new_user).execute()
    return {"message": "Usuario creado exitosamente", "user": response.data[0]}

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    supabase = get_supabase()
    
    existing = supabase.table("users").select("*").eq("id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    
    # Si se actualiza la contraseña, hashearla
    if "hashed_password" in update_data:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(update_data["hashed_password"].encode('utf-8'), salt)
        update_data["hashed_password"] = hashed.decode('utf-8')
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    response = supabase.table("users").update(update_data).eq("id", user_id).execute()
    return {"message": "Usuario actualizado exitosamente", "user": response.data[0]}

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    supabase = get_supabase()
    
    existing = supabase.table("users").select("*").eq("id", user_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_id == 1:
        raise HTTPException(status_code=403, detail="No se puede eliminar al administrador principal")
    
    supabase.table("users").delete().eq("id", user_id).execute()
    return {"message": "Usuario eliminado exitosamente"}