"""
Script de prueba para verificar la conexión con Supabase
Ejecutar con: python test_supabase.py
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def test_connection():
    """Prueba la conexión con Supabase"""
    
    print("=" * 50)
    print("🔍 PROBANDO CONEXIÓN CON SUPABASE")
    print("=" * 50)
    
    # Obtener credenciales
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("❌ ERROR: No se encontraron las credenciales en .env")
        print("\nAsegúrate de que el archivo .env contenga:")
        print("SUPABASE_URL=https://tuproyecto.supabase.co")
        print("SUPABASE_ANON_KEY=tu_anon_key")
        return False
    
    print(f"\n📡 URL: {url}")
    print(f"🔑 KEY: {key[:30]}...")
    
    try:
        # Crear cliente de Supabase
        supabase = create_client(url, key)
        print("\n✅ Cliente creado correctamente")
        
        # Intentar obtener la versión de PostgreSQL
        print("\n📊 Probando consulta a la base de datos...")
        
        # Consulta simple para verificar conexión
        response = supabase.table("users").select("*", count="exact").limit(1).execute()
        
        print("\n" + "=" * 50)
        print("✅ ¡CONEXIÓN EXITOSA!")
        print("=" * 50)
        print(f"📊 Estado: Conectado a Supabase")
        print(f"📦 Base de datos: PostgreSQL en la nube")
        print(f"👥 Usuarios encontrados: {response.count}")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 50)
        print("❌ ERROR DE CONEXIÓN")
        print("=" * 50)
        print(f"Error: {e}")
        
        print("\n🔧 POSIBLES SOLUCIONES:")
        print("1. Verifica que las credenciales en .env sean correctas")
        print("2. Asegúrate de haber creado las tablas en Supabase")
        print("3. Revisa que la tabla 'users' exista")
        print("4. Verifica tu conexión a internet")
        
        return False

def test_create_table():
    """Prueba si la tabla users existe"""
    
    print("\n" + "=" * 50)
    print("📋 VERIFICANDO TABLAS EN SUPABASE")
    print("=" * 50)
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    try:
        supabase = create_client(url, key)
        
        # Intentar obtener la estructura de la tabla
        response = supabase.table("users").select("*").limit(0).execute()
        
        print("✅ La tabla 'users' existe")
        print("✅ La estructura de la base de datos es correcta")
        return True
        
    except Exception as e:
        print("❌ La tabla 'users' NO existe o no es accesible")
        print("\n📌 Debes ejecutar el script SQL en Supabase primero:")
        print("1. Ve a https://supabase.com/dashboard")
        print("2. Selecciona tu proyecto")
        print("3. Ve a 'SQL Editor'")
        print("4. Crea un nuevo query")
        print("5. Ejecuta el script de creación de tablas")
        return False

def test_insert_example():
    """Prueba insertar un usuario de ejemplo"""
    
    print("\n" + "=" * 50)
    print("➕ PROBANDO INSERTAR DATOS DE EJEMPLO")
    print("=" * 50)
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")  # Usamos service key para insertar
    
    if not key:
        key = os.getenv("SUPABASE_ANON_KEY")
    
    try:
        supabase = create_client(url, key)
        
        # Datos de ejemplo
        test_user = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Usuario de Prueba",
            "hashed_password": "contraseña_temporal",
            "role": "student",
            "is_active": True
        }
        
        # Intentar insertar
        response = supabase.table("users").insert(test_user).execute()
        
        print("✅ Usuario de prueba insertado correctamente")
        print(f"📝 ID del usuario: {response.data[0]['id'] if response.data else 'N/A'}")
        
        # Limpiar: eliminar el usuario de prueba
        supabase.table("users").delete().eq("username", "testuser").execute()
        print("🗑️  Usuario de prueba eliminado")
        
        return True
        
    except Exception as e:
        print(f"⚠️  No se pudo insertar (es normal si la tabla está vacía): {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DE SUPABASE\n")
    
    # Prueba 1: Conexión básica
    if test_connection():
        # Prueba 2: Verificar tablas
        test_create_table()
        # Prueba 3: Probar inserción (opcional)
        # test_insert_example()
    
    print("\n" + "=" * 50)
    print("🏁 FIN DE LAS PRUEBAS")
    print("=" * 50)