"""
PRUEBAS DE INTEGRIDAD DEL SISTEMA UNIVERSITARIO
Ejecutar con: python test_integridad.py
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000/api"
TEST_USER = {"username": "admin", "password": "admin123"}

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name, passed, message=""):
    status = f"{Colors.GREEN}✅ PASÓ{Colors.RESET}" if passed else f"{Colors.RED}❌ FALLÓ{Colors.RESET}"
    print(f"{status} - {name}")
    if message and not passed:
        print(f"     {Colors.YELLOW}⚠️ {message}{Colors.RESET}")

def test_connection():
    """Prueba 1: Conexión al servidor"""
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_login():
    """Prueba 2: Autenticación"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=TEST_USER)
        if response.status_code == 200:
            data = response.json()
            return True, data.get('user', {})
        return False, None
    except:
        return False, None

def test_get_users():
    """Prueba 3: Obtener usuarios"""
    try:
        response = requests.get(f"{BASE_URL}/users")
        return response.status_code == 200
    except:
        return False

def test_get_periods():
    """Prueba 4: Obtener períodos"""
    try:
        response = requests.get(f"{BASE_URL}/periods")
        return response.status_code == 200
    except:
        return False

def test_get_grades():
    """Prueba 5: Obtener calificaciones"""
    try:
        response = requests.get(f"{BASE_URL}/grades")
        return response.status_code == 200
    except:
        return False

def test_create_user():
    """Prueba 6: Crear usuario temporal"""
    try:
        new_user = {
            "email": f"test_{datetime.now().timestamp()}@test.com",
            "username": f"testuser_{datetime.now().timestamp()}",
            "full_name": "Usuario de Prueba",
            "password": "test123",
            "role": "student"
        }
        response = requests.post(f"{BASE_URL}/users", json=new_user)
        return response.status_code in [200, 201]
    except:
        return False

def test_student_grades_endpoint():
    """Prueba 7: Endpoint de calificaciones por estudiante"""
    try:
        # Obtener un estudiante
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users = response.json().get('users', [])
            student = next((u for u in users if u.get('role') == 'student'), None)
            if student:
                student_id = student['id']
                response = requests.get(f"{BASE_URL}/grades/student/{student_id}")
                return response.status_code == 200
        return False
    except:
        return False

def test_cors_headers():
    """Prueba 8: Headers CORS"""
    try:
        response = requests.options(f"{BASE_URL}/auth/login", 
                                   headers={"Origin": "http://localhost:5173"})
        return 'access-control-allow-origin' in response.headers
    except:
        return False

def test_database_connection():
    """Prueba 9: Conexión a Supabase"""
    try:
        from app.database import get_supabase
        supabase = get_supabase()
        response = supabase.table('users').select('count').execute()
        return True
    except Exception as e:
        print(f"     Error: {e}")
        return False

def test_rate_limit():
    """Prueba 10: Rate limiting"""
    try:
        # Hacer múltiples peticiones rápidas
        for i in range(6):
            response = requests.post(f"{BASE_URL}/auth/login", 
                                    json={"username": "wrong", "password": "wrong"})
            if response.status_code == 429:
                return True
        return False
    except:
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🔍 PRUEBAS DE INTEGRIDAD DEL SISTEMA{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    results = []
    
    # Ejecutar pruebas
    print(f"{Colors.YELLOW}📡 Conectando al servidor...{Colors.RESET}")
    results.append(("Conexión al servidor", test_connection()))
    
    print(f"{Colors.YELLOW}🔐 Probando autenticación...{Colors.RESET}")
    login_ok, user = test_login()
    results.append(("Autenticación de usuario", login_ok))
    
    if user:
        print(f"     👤 Usuario: {user.get('full_name')} ({user.get('role')})")
    
    print(f"{Colors.YELLOW}📋 Probando endpoints...{Colors.RESET}")
    results.append(("GET /users", test_get_users()))
    results.append(("GET /periods", test_get_periods()))
    results.append(("GET /grades", test_get_grades()))
    results.append(("POST /users (crear)", test_create_user()))
    results.append(("GET /grades/student/{id}", test_student_grades_endpoint()))
    results.append(("Headers CORS", test_cors_headers()))
    results.append(("Conexión a Supabase", test_database_connection()))
    results.append(("Rate limiting (429)", test_rate_limit()))
    
    # Mostrar resultados
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}📊 RESULTADOS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    passed = 0
    for name, result in results:
        print_test(name, result)
        if result:
            passed += 1
    
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"📈 Total: {passed}/{total} pruebas exitosas ({percentage:.1f}%)")
    
    if percentage == 100:
        print(f"{Colors.GREEN}✅ ¡TODAS LAS PRUEBAS PASARON! El sistema está íntegro.{Colors.RESET}")
    elif percentage >= 80:
        print(f"{Colors.YELLOW}⚠️ La mayoría de pruebas pasaron. Revisar las fallidas.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Múltiples fallos. Revisar configuración.{Colors.RESET}")
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

if __name__ == "__main__":
    main()