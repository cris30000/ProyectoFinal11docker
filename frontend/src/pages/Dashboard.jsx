import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalStudents: 0,
    totalTeachers: 0,
    totalPeriods: 0,
    activePeriod: null,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const usersRes = await api.get('/users');
      const periodsRes = await api.get('/periods');
      
      const students = usersRes.data.users.filter(u => u.role === 'student');
      const teachers = usersRes.data.users.filter(u => u.role === 'teacher');
      const activePeriod = periodsRes.data.periods.find(p => p.is_active);
      
      setStats({
        totalStudents: students.length,
        totalTeachers: teachers.length,
        totalPeriods: periodsRes.data.periods.length,
        activePeriod: activePeriod,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">Cargando dashboard...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">
        Dashboard - Bienvenido, {user?.full_name}
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center">
            <div className="text-3xl mr-3">👥</div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">Total Estudiantes</h3>
              <p className="text-3xl font-bold text-blue-600">{stats.totalStudents}</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="text-3xl mr-3">👨‍🏫</div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">Total Docentes</h3>
              <p className="text-3xl font-bold text-green-600">{stats.totalTeachers}</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="text-3xl mr-3">📅</div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">Períodos</h3>
              <p className="text-3xl font-bold text-purple-600">{stats.totalPeriods}</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="text-3xl mr-3">✅</div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">Período Activo</h3>
              <p className="text-xl font-semibold text-orange-600">
                {stats.activePeriod?.name || 'Ninguno'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-bold mb-4">Información del Sistema</h2>
        <p className="text-gray-600">
          Sistema de Gestión Universitaria funcionando correctamente ✅
        </p>
        <p className="text-gray-600 mt-2">
          Tu rol actual es: <strong>{user?.role}</strong>
        </p>
      </div>
    </div>
  );
};

export default Dashboard;