# 🎓 Sistema de universidad

Sistema de gestión universitaria completo con autenticación segura, gestión de usuarios, períodos académicos y calificaciones.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Ejecución](#-ejecución)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Pruebas](#-pruebas)
- [Solución de Problemas](#-solución-de-problemas)
- [Despliegue](#-despliegue)

## ✨ Características

### 🔐 Seguridad

- Autenticación JWT con refresh tokens
- Contraseñas hasheadas con bcrypt
- Rate limiting (5 intentos/minuto)(salio error)
- Headers CORS configurados
- Protección contra fuerza bruta

### 👥 Gestión de Usuarios

- CRUD completo de usuarios
- Roles: Admin, Teacher, Student
- Cambio de contraseña
- Perfiles de usuario

### 📅 Gestión Académica

- Períodos académicos
- Asignación de materias
- Registro de calificaciones
- Promedios automáticos

### 📊 Dashboard

- Estadísticas en tiempo real
- Gráficos de rendimiento
- Resumen por materias
- Indicadores visuales

## 🛠 Tecnologías

### Backend

| Tecnología  | Versión | Propósito                |
| ----------- | ------- | ------------------------ |
| Python      | 3.11    | Lenguaje principal       |
| FastAPI     | 0.104.1 | Framework API            |
| Supabase    | -       | Base de datos en la nube |
| bcrypt      | 4.0.1   | Hash de contraseñas      |
| python-jose | 3.3.0   | JWT tokens               |

### Frontend

| Tecnología   | Versión | Propósito    |
| ------------ | ------- | ------------ |
| React        | 18.2.0  | UI Framework |
| Vite         | 5.0.0   | Build tool   |
| TailwindCSS  | 3.4.0   | Estilos      |
| Axios        | 1.6.0   | HTTP client  |
| React Router | 6.20.0  | Navegación   |

## 📦 Requisitos Previos

- **Python 3.11** o superior
- **Node.js 18** o superior
- **npm** o **yarn**
- **Git** (opcional)
- **Cuenta en Supabase** (gratis)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/university-system.git
cd university-system


/////////////////////////////////
configurar backend

# Crear entorno virtual (Windows)
python -m venv venv
venv\Scripts\activate


# Instalar dependencias
pip install -r requirements.txt

/// configurar Frontend
npm install

// variables de entorno
# SUPABASE CREDENTIALS
# ============================================
SUPABASE_URL=https://ssvgnlhissnudfexyzmh.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzdmdubGhpc3NudWRmZXh5em1oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDM3OTcsImV4cCI6MjA5MTcxOTc5N30.93VoD6JxgGLQVK09OwIgEGZWrANNlfiockZA4mwHJKU
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzdmdubGhpc3NudWRmZXh5em1oIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjE0Mzc5NywiZXhwIjoyMDkxNzE5Nzk3fQ.QS_mQKAqvFBdIiFqZtyfQ-7s4yoxwLS1IxzWB4bSyGE

# ============================================
# DATABASE CONNECTION (para SQLAlchemy)
# ============================================
# IMPORTANTE: Cambia 'TU_CONTRASEÑA' por la contraseña que creaste al iniciar el proyecto
DATABASE_URL=postgresql://postgres:UniversidadCris24@db.ssvgnlhisnudfexyzmh.supabase.co:5432/postgres

# ============================================
# JWT SECURITY (para tu backend)
# ============================================
SECRET_KEY=mi-clave-secreta-super-segura-para-jwt-2025
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# CORS (para frontend)
# ============================================
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```
