import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Grades = () => {
  const [grades, setGrades] = useState([]);
  const [students, setStudents] = useState([]);
  const [periods, setPeriods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingGrade, setEditingGrade] = useState(null);
  const [formData, setFormData] = useState({
    student_id: '',
    period_id: '',
    subject: '',
    grade_value: '',
    observation: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [gradesRes, usersRes, periodsRes] = await Promise.all([
        api.get('/grades'),
        api.get('/users'),
        api.get('/periods')
      ]);
      setGrades(gradesRes.data.grades);
      setStudents(usersRes.data.users.filter(u => u.role === 'student'));
      setPeriods(periodsRes.data.periods);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingGrade) {
        await api.put(`/grades/${editingGrade.id}`, {
          grade_value: parseFloat(formData.grade_value),
          observation: formData.observation
        });
      } else {
        await api.post('/grades', {
          ...formData,
          grade_value: parseFloat(formData.grade_value)
        });
      }
      setShowModal(false);
      resetForm();
      fetchData();
    } catch (error) {
      console.error('Error saving grade:', error);
      alert(error.response?.data?.detail || 'Error al guardar calificación');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Eliminar esta calificación?')) {
      try {
        await api.delete(`/grades/${id}`);
        fetchData();
      } catch (error) {
        console.error('Error deleting grade:', error);
        alert(error.response?.data?.detail || 'Error al eliminar calificación');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      student_id: '',
      period_id: '',
      subject: '',
      grade_value: '',
      observation: ''
    });
    setEditingGrade(null);
  };

  const openCreateModal = () => {
    resetForm();
    setShowModal(true);
  };

  const openEditModal = (grade) => {
    setEditingGrade(grade);
    setFormData({
      student_id: grade.student_id,
      period_id: grade.period_id,
      subject: grade.subject,
      grade_value: grade.grade_value,
      observation: grade.observation || ''
    });
    setShowModal(true);
  };

  if (loading) {
    return <div className="text-center py-8">Cargando calificaciones...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Calificaciones</h1>
        <button onClick={openCreateModal} className="btn-primary">
          + Nueva Calificación
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estudiante</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Período</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Materia</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nota</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Observación</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {grades.map((grade) => (
              <tr key={grade.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {grade.users?.full_name || `ID: ${grade.student_id}`}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {grade.periods?.name || `ID: ${grade.period_id}`}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{grade.subject}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    grade.grade_value >= 60 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {grade.grade_value}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">{grade.observation}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button onClick={() => openEditModal(grade)} className="text-blue-600 hover:text-blue-900 mr-3">
                    Editar
                  </button>
                  <button onClick={() => handleDelete(grade.id)} className="text-red-600 hover:text-red-900">
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {editingGrade ? 'Editar Calificación' : 'Nueva Calificación'}
              </h3>
              <button onClick={() => setShowModal(false)} className="text-gray-400 hover:text-gray-600">✕</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Estudiante</label>
                  <select
                    required
                    value={formData.student_id}
                    onChange={(e) => setFormData({...formData, student_id: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    disabled={editingGrade}
                  >
                    <option value="">Seleccionar</option>
                    {students.map(s => (
                      <option key={s.id} value={s.id}>{s.full_name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Período</label>
                  <select
                    required
                    value={formData.period_id}
                    onChange={(e) => setFormData({...formData, period_id: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    disabled={editingGrade}
                  >
                    <option value="">Seleccionar</option>
                    {periods.map(p => (
                      <option key={p.id} value={p.id}>{p.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Materia</label>
                  <input
                    type="text"
                    required
                    value={formData.subject}
                    onChange={(e) => setFormData({...formData, subject: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    disabled={editingGrade}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Nota (0-100)</label>
                  <input
                    type="number"
                    required
                    min="0"
                    max="100"
                    step="0.01"
                    value={formData.grade_value}
                    onChange={(e) => setFormData({...formData, grade_value: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Observación</label>
                  <textarea
                    rows="3"
                    value={formData.observation}
                    onChange={(e) => setFormData({...formData, observation: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="mt-6 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowModal(false)} className="btn-danger">Cancelar</button>
                <button type="submit" className="btn-primary">{editingGrade ? 'Actualizar' : 'Crear'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Grades;