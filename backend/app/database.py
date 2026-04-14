import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Usamos service_key para el backend

# Verificar que las variables existen
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Faltan variables de entorno: SUPABASE_URL o SUPABASE_KEY")

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase():
    """Retorna el cliente de Supabase para usar en los routers"""
    return supabase

# Mantener get_db por compatibilidad (opcional)
async def get_db():
    """Para compatibilidad con código existente"""
    return supabase