import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600">
      <div className="max-w-md w-full text-center p-8 bg-white rounded-lg shadow-2xl">
        {/* Icono 404 */}
        <div className="text-8xl mb-4">🔍</div>
        
        {/* Código de error */}
        <h1 className="text-9xl font-bold text-gray-800 mb-4">404</h1>
        
        {/* Mensaje principal */}
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">
          Página no encontrada
        </h2>
        
        {/* Descripción */}
        <p className="text-gray-500 mb-6">
          Lo sentimos, la página que estás buscando no existe o ha sido movida.
        </p>
        
        {/* Posibles causas */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6 text-left">
          <p className="text-sm text-gray-600 mb-2">🔍 Posibles causas:</p>
          <ul className="text-sm text-gray-500 list-disc list-inside space-y-1">
            <li>La URL puede estar mal escrita</li>
            <li>La página fue eliminada o movida</li>
            <li>El enlace que usaste está desactualizado</li>
          </ul>
        </div>
        
        {/* Botón para volver al inicio */}
        <Link
          to="/dashboard"
          className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          🏠 Volver al Dashboard
        </Link>
        
        {/* Enlace a login alternativo */}
        <div className="mt-4">
          <Link
            to="/login"
            className="text-sm text-gray-500 hover:text-gray-700"
          >
            🔐 Ir a la página de inicio de sesión
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;