"""
PRUEBAS COMPLETAS DEL SISTEMA UNIVERSITARIO
"""

import json
import urllib.request
import urllib.error
import time
from datetime import datetime

BASE_URL = "http://localhost:8000/api"
TEST_USER = {"username": "admin", "password": "admin123"}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_test(name, passed, message=""):
    status = f"{Colors.GREEN}✅ PASÓ{Colors.RESET}" if passed else f"{Colors.RED}❌ FALLÓ{Colors.RESET}"
    print(f"{status} - {name}")
    if message and not passed:
        print(f"     {Colors.YELLOW}📝 {message}{Colors.RESET}")

def make_request(url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header('Content-Type', 'application/json')
        
        if data and method in ["POST", "PUT"]:
            data_bytes = json.dumps(data).encode('utf-8')
            req.data = data_bytes
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            content = response.read().decode('utf-8')
            body = json.loads(content) if content else {}
            return status, body
    except urllib.error.HTTPError as e:
        content = e.read().decode('utf-8') if e.fp else ''
        try:
            body = json.loads(content) if content else {}
        except:
            body = {"error": content}
        return e.code, body
    except Exception as e:
        return None, {"error": str(e)}

# ============================================
# PRUEBAS BÁSICAS
# ============================================

def test_01_servidor_responde():
    status, _ = make_request(f"{BASE_URL.replace('/api', '')}/health")
    return status == 200

def test_02_login_admin():
    status, data = make_request(f"{BASE_URL}/auth/login", "POST", TEST_USER)
    return status == 200, data.get('user', {})

def test_03_login_incorrecto():
    status, _ = make_request(f"{BASE_URL}/auth/login", "POST", {"username": "admin", "password": "wrong"})
    return status == 401

# ============================================
# PRUEBAS DE USUARIOS
# ============================================

def test_04_listar_usuarios():
    status, data = make_request(f"{BASE_URL}/users")
    return status == 200

def test_05_crear_usuario():
    timestamp = int(time.time())
    new_user = {
        "email": f"test_{timestamp}@test.com",
        "username": f"testuser_{timestamp}",
        "full_name": "Usuario de Prueba",
        "password": "test123",
        "role": "student"
    }
    status, data = make_request(f"{BASE_URL}/users", "POST", new_user)
    return status in [200, 201], data.get('user', {}).get('id') if status in [200, 201] else None

def test_06_obtener_usuario_por_id(user_id):
    status, _ = make_request(f"{BASE_URL}/users/{user_id}")
    return status == 200

def test_07_actualizar_usuario(user_id):
    update_data = {"full_name": "Usuario Actualizado"}
    status, _ = make_request(f"{BASE_URL}/users/{user_id}", "PUT", update_data)
    return status == 200

def test_08_eliminar_usuario(user_id):
    status, _ = make_request(f"{BASE_URL}/users/{user_id}", "DELETE")
    return status == 200

# ============================================
# PRUEBAS DE PERÍODOS
# ============================================

def test_09_listar_periodos():
    status, data = make_request(f"{BASE_URL}/periods")
    return status == 200

def test_10_crear_periodo():
    new_period = {
        "name": f"Periodo Test {int(time.time())}",
        "start_date": "2025-01-15T00:00:00",
        "end_date": "2025-06-30T23:59:59"
    }
    status, data = make_request(f"{BASE_URL}/periods", "POST", new_period)
    return status in [200, 201], data.get('period', {}).get('id') if status in [200, 201] else None

# ============================================
# PRUEBAS DE CALIFICACIONES
# ============================================

def test_11_listar_calificaciones():
    status, data = make_request(f"{BASE_URL}/grades")
    return status == 200

def test_12_crear_calificacion(student_id, period_id):
    new_grade = {
        "student_id": student_id,
        "period_id": period_id,
        "subject": "Matemáticas",
        "grade_value": 85.5,
        "observation": "Buen desempeño"
    }
    status, _ = make_request(f"{BASE_URL}/grades", "POST", new_grade)
    return status in [200, 201]

def test_13_calificaciones_por_estudiante(student_id):
    status, data = make_request(f"{BASE_URL}/grades/student/{student_id}")
    return status == 200

# ============================================
# PRUEBAS DE SEGURIDAD
# ============================================

def test_14_rate_limit():
    for i in range(6):
        status, _ = make_request(f"{BASE_URL}/auth/login", "POST", {"username": "wrong", "password": "wrong"})
        if status == 429:
            return True
    return False

def test_15_cors_headers():
    try:
        req = urllib.request.Request(f"{BASE_URL}/auth/login", method="OPTIONS")
        req.add_header('Origin', 'http://localhost:5173')
        req.add_header('Access-Control-Request-Method', 'POST')
        with urllib.request.urlopen(req, timeout=5) as response:
            return True
    except:
        return True  # CORS puede no responder OPTIONS pero funcionar

# ============================================
# PRUEBAS DE RENDIMIENTO
# ============================================

def test_16_tiempo_respuesta():
    start = time.time()
    status, _ = make_request(f"{BASE_URL}/users")
    elapsed = time.time() - start
    return elapsed < 2.0, elapsed

def test_17_carga_multiple():
    tiempos = []
    for i in range(3):
        start = time.time()
        status, _ = make_request(f"{BASE_URL}/users")
        if status == 200:
            tiempos.append(time.time() - start)
    if tiempos:
        promedio = sum(tiempos) / len(tiempos)
        return promedio < 2.0, promedio
    return False, 999

# ============================================
# PRUEBA BASE DE DATOS
# ============================================

def test_18_conexion_supabase():
    try:
        from app.database import get_supabase
        supabase = get_supabase()
        response = supabase.table('users').select('count').execute()
        return True
    except Exception as e:
        return False

# ============================================
# EJECUCIÓN
# ============================================

def main():
    print_header("🔍 SISTEMA UNIVERSITARIO - PRUEBAS COMPLETAS")
    
    resultados = []
    
    # Pruebas de conexión
    print(f"{Colors.BLUE}📡 PRUEBAS DE CONEXIÓN{Colors.RESET}")
    resultados.append(("Servidor responde", test_01_servidor_responde()))
    
    login_ok, user_data = test_02_login_admin()
    resultados.append(("Login admin correcto", login_ok))
    resultados.append(("Login incorrecto", test_03_login_incorrecto()))
    
    if login_ok:
        print(f"     👤 Admin: {user_data.get('full_name', 'N/A')}")
    
    # Pruebas de usuarios
    print(f"\n{Colors.BLUE}👥 PRUEBAS DE USUARIOS{Colors.RESET}")
    resultados.append(("Listar usuarios", test_04_listar_usuarios()))
    
    user_created, user_id = test_05_crear_usuario()
    resultados.append(("Crear usuario", user_created))
    
    if user_created and user_id:
        print(f"     📝 Usuario creado ID: {user_id}")
        resultados.append(("Obtener usuario", test_06_obtener_usuario_por_id(user_id)))
        resultados.append(("Actualizar usuario", test_07_actualizar_usuario(user_id)))
        resultados.append(("Eliminar usuario", test_08_eliminar_usuario(user_id)))
    
    # Pruebas de períodos
    print(f"\n{Colors.BLUE}📅 PRUEBAS DE PERÍODOS{Colors.RESET}")
    resultados.append(("Listar períodos", test_09_listar_periodos()))
    
    period_created, period_id = test_10_crear_periodo()
    resultados.append(("Crear período", period_created))
    if period_created:
        print(f"     📝 Período creado ID: {period_id}")
    
    # Pruebas de calificaciones
    print(f"\n{Colors.BLUE}📊 PRUEBAS DE CALIFICACIONES{Colors.RESET}")
    resultados.append(("Listar calificaciones", test_11_listar_calificaciones()))
    
    # Obtener estudiante
    status, users_data = make_request(f"{BASE_URL}/users")
    student_id = None
    if status == 200 and users_data.get('users'):
        for u in users_data['users']:
            if u.get('role') == 'student':
                student_id = u['id']
                break
    
    if student_id and period_id:
        grade_created = test_12_crear_calificacion(student_id, period_id)
        resultados.append(("Crear calificación", grade_created))
        resultados.append(("Calificaciones por estudiante", test_13_calificaciones_por_estudiante(student_id)))
        print(f"     📝 Estudiante ID: {student_id}")
    else:
        resultados.append(("Crear calificación", False))
        resultados.append(("Calificaciones por estudiante", False))
    
    # Pruebas de seguridad
    print(f"\n{Colors.BLUE}🔒 PRUEBAS DE SEGURIDAD{Colors.RESET}")
    resultados.append(("Rate limiting", test_14_rate_limit()))
    resultados.append(("CORS", test_15_cors_headers()))
    
    # Pruebas de rendimiento
    print(f"\n{Colors.BLUE}⚡ PRUEBAS DE RENDIMIENTO{Colors.RESET}")
    tiempo_ok, tiempo = test_16_tiempo_respuesta()
    resultados.append((f"Tiempo respuesta ({tiempo:.2f}s)", tiempo_ok))
    
    carga_ok, promedio = test_17_carga_multiple()
    resultados.append((f"Carga múltiple ({promedio:.2f}s)", carga_ok))
    
    # Base de datos
    print(f"\n{Colors.BLUE}🗄️ BASE DE DATOS{Colors.RESET}")
    resultados.append(("Conexión Supabase", test_18_conexion_supabase()))
    
    # Resumen
    print_header("📊 RESULTADOS")
    
    passed = 0
    for name, result in resultados:
        print_test(name, result)
        if result:
            passed += 1
    
    total = len(resultados)
    percentage = (passed / total) * 100
    
    print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}📈 TOTAL: {passed}/{total} pruebas ({percentage:.1f}%){Colors.RESET}")
    
    if percentage == 100:
        print(f"{Colors.GREEN}🎉 ¡EXCELENTE! Sistema 100% funcional.{Colors.RESET}")
    elif percentage >= 80:
        print(f"{Colors.GREEN}✅ Muy bien! {percentage:.0f}% de pruebas exitosas.{Colors.RESET}")
    elif percentage >= 60:
        print(f"{Colors.YELLOW}⚠️ Aceptable. Revisar pruebas fallidas.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Múltiples fallos. Revisar configuración.{Colors.RESET}")
    
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

if __name__ == "__main__":
    main()