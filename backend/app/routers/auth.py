from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database import get_supabase
import bcrypt

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(login_data: LoginRequest):
    supabase = get_supabase()
    
    # Buscar usuario por username
    response = supabase.table("users").select("*").eq("username", login_data.username).execute()
    
    # ============================================
    # CASO 1: USUARIO NO EXISTE
    # ============================================
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ Usuario no encontrado. Verifica tu nombre de usuario."
        )
    
    user = response.data[0]
    stored_password = user.get("hashed_password", "")
    
    # ============================================
    # CASO 2: VERIFICAR CONTRASEÑA
    # ============================================
    
    # Verificar si es un hash bcrypt (comienza con $2b$)
    if stored_password.startswith('$2b$'):
        # Es un hash bcrypt - verificar
        try:
            if bcrypt.checkpw(login_data.password.encode('utf-8'), stored_password.encode('utf-8')):
                # ============================================
                # CASO 3: LOGIN EXITOSO
                # ============================================
                return {
                    "message": f"✅ Bienvenido {user['full_name']}",
                    "user": {
                        "id": user["id"],
                        "username": user["username"],
                        "email": user["email"],
                        "full_name": user["full_name"],
                        "role": user["role"]
                    }
                }
            else:
                # Contraseña incorrecta
                raise HTTPException(
                    status_code=401, 
                    detail="❌ Contraseña incorrecta. Por favor, inténtalo de nuevo."
                )
        except Exception as e:
            print(f"Error verificando bcrypt: {e}")
            raise HTTPException(
                status_code=401, 
                detail="❌ Error al verificar la contraseña. Contacta al administrador."
            )
    else:
        # Es texto plano - intentar convertir a hash automáticamente
        try:
            # Intentar verificar como texto plano
            if login_data.password == stored_password:
                # Convertir a hash bcrypt
                salt = bcrypt.gensalt(rounds=12)
                new_hash = bcrypt.hashpw(login_data.password.encode('utf-8'), salt)
                
                # Actualizar en la base de datos
                supabase.table("users").update({"hashed_password": new_hash.decode('utf-8')}).eq("id", user["id"]).execute()
                
                print(f"✅ Contraseña de {user['username']} convertida a hash bcrypt")
                
                return {
                    "message": f"✅ Bienvenido {user['full_name']}",
                    "user": {
                        "id": user["id"],
                        "username": user["username"],
                        "email": user["email"],
                        "full_name": user["full_name"],
                        "role": user["role"]
                    }
                }
            else:
                # Contraseña incorrecta
                raise HTTPException(
                    status_code=401, 
                    detail="❌ Contraseña incorrecta. Por favor, inténtalo de nuevo."
                )
        except:
            raise HTTPException(
                status_code=401, 
                detail="❌ Error al verificar la contraseña. Contacta al administrador."
            )