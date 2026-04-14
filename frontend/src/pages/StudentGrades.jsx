import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const StudentGrades = () => {
  const { user } = useAuth();
  const [grades, setGrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [average, setAverage] = useState(0);
  const [summary, setSummary] = useState({});

  useEffect(() => {
    fetchMyGrades();
  }, []);

  const fetchMyGrades = async () => {
    try {
      const response = await api.get(`/grades/student/${user.id}`);
      setGrades(response.data.grades);
      
      // Calcular promedio
      if (response.data.grades.length > 0) {
        const total = response.data.grades.reduce((sum, g) => sum + g.grade_value, 0);
        const avg = total / response.data.grades.length;
        setAverage(avg);
        
        // Resumen por materia
        const subjectSummary = {};
        response.data.grades.forEach(g => {
          if (!subjectSummary[g.subject]) {
            subjectSummary[g.subject] = {
              grades: [],
              average: 0
            };
          }
          subjectSummary[g.subject].grades.push(g.grade_value);
          subjectSummary[g.subject].average = 
            subjectSummary[g.subject].grades.reduce((a, b) => a + b, 0) / 
            subjectSummary[g.subject].grades.length;
        });
        setSummary(subjectSummary);
      }
    } catch (error) {
      console.error('Error fetching grades:', error);
    } finally {
      setLoading(false);
    }
  };

  const getGradeColor = (grade) => {
    if (grade >= 90) return 'text-green-600';
    if (grade >= 70) return 'text-blue-600';
    if (grade >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getGradeBadge = (grade) => {
    if (grade >= 90) return 'bg-green-100 text-green-800';
    if (grade >= 70) return 'bg-blue-100 text-blue-800';
    if (grade >= 60) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">Cargando calificaciones...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Mis Calificaciones</h1>
      
      {/* Tarjeta de promedio general */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow p-6 text-white">
        <h2 className="text-xl font-semibold mb-2">Promedio General</h2>
        <p className="text-5xl font-bold">{average.toFixed(1)}</p>
        <p className="text-sm mt-2">Total de calificaciones: {grades.length}</p>
      </div>

      {/* Resumen por materia */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Resumen por Materia</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(summary).map(([subject, data]) => (
            <div key={subject} className="border rounded-lg p-4">
              <h3 className="font-semibold text-gray-900">{subject}</h3>
              <p className={`text-2xl font-bold ${getGradeColor(data.average)}`}>
                {data.average.toFixed(1)}
              </p>
              <p className="text-sm text-gray-500">Calificaciones: {data.grades.length}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Tabla de calificaciones */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <h2 className="text-xl font-bold text-gray-900 p-6 pb-0">Detalle de Calificaciones</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Materia
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Período
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nota
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Observación
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {grades.map((grade) => (
                <tr key={grade.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {grade.subject}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {grade.periods?.name || `ID: ${grade.period_id}`}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`text-lg font-bold ${getGradeColor(grade.grade_value)}`}>
                      {grade.grade_value}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getGradeBadge(grade.grade_value)}`}>
                      {grade.grade_value >= 60 ? 'Aprobado' : 'Reprobado'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                    {grade.observation || '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {grades.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No hay calificaciones registradas aún.
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentGrades;