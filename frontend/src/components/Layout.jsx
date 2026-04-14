import React, { useState, useEffect } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Layout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [rateLimitInfo, setRateLimitInfo] = useState(null);

  // Efecto para escuchar errores de rate limit
  useEffect(() => {
    const handleRateLimit = (event) => {
      if (event.detail?.status === 429) {
        setRateLimitInfo(event.detail);
        setTimeout(() => setRateLimitInfo(null), 60000);
      }
    };
    
    window.addEventListener('rate-limit', handleRateLimit);
    return () => window.removeEventListener('rate-limit', handleRateLimit);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex space-x-8">
              <Link to="/dashboard" className="flex items-center text-gray-700 hover:text-gray-900">
                🏫 Dashboard
              </Link>
              {user?.role === 'admin' && (
                <>
                  <Link to="/users" className="flex items-center text-gray-700 hover:text-gray-900">
                    👥 Usuarios
                  </Link>
                  <Link to="/periods" className="flex items-center text-gray-700 hover:text-gray-900">
                    📅 Períodos
                  </Link>
                </>
              )}
              {(user?.role === 'teacher' || user?.role === 'admin') && (
                <Link to="/grades" className="flex items-center text-gray-700 hover:text-gray-900">
                  📊 Calificaciones
                </Link>
              )}
              {/* ✅ NUEVO: Enlace para estudiantes - MIS CALIFICACIONES */}
              {user?.role === 'student' && (
                <Link to="/my-grades" className="flex items-center text-gray-700 hover:text-gray-900">
                  📋 Mis Calificaciones
                </Link>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                {user?.full_name} ({user?.role})
              </span>
              <button
                onClick={handleLogout}
                className="px-3 py-1 text-sm text-red-600 hover:text-red-800"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <Outlet />
      </main>

      {/* Notificación de rate limit */}
      {rateLimitInfo && (
        <div className="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50">
          ⚠️ Demasiadas solicitudes. Espera {rateLimitInfo.wait_time} segundos.
        </div>
      )}
    </div>
  );
};

export default Layout;