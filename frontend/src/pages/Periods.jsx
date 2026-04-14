import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Periods = () => {
  const [periods, setPeriods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingPeriod, setEditingPeriod] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    start_date: '',
    end_date: ''
  });

  useEffect(() => {
    fetchPeriods();
  }, []);

  const fetchPeriods = async () => {
    try {
      const response = await api.get('/periods');
      setPeriods(response.data.periods);
    } catch (error) {
      console.error('Error fetching periods:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingPeriod) {
        await api.put(`/periods/${editingPeriod.id}`, formData);
      } else {
        await api.post('/periods', formData);
      }
      setShowModal(false);
      resetForm();
      fetchPeriods();
    } catch (error) {
      console.error('Error saving period:', error);
      alert(error.response?.data?.detail || 'Error al guardar período');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Eliminar este período?')) {
      try {
        await api.delete(`/periods/${id}`);
        fetchPeriods();
      } catch (error) {
        console.error('Error deleting period:', error);
        alert(error.response?.data?.detail || 'Error al eliminar período');
      }
    }
  };

  const resetForm = () => {
    setFormData({ name: '', start_date: '', end_date: '' });
    setEditingPeriod(null);
  };

  const openCreateModal = () => {
    resetForm();
    setShowModal(true);
  };

  const openEditModal = (period) => {
    setEditingPeriod(period);
    setFormData({
      name: period.name,
      start_date: period.start_date.slice(0, 16),
      end_date: period.end_date.slice(0, 16)
    });
    setShowModal(true);
  };

  if (loading) {
    return <div className="text-center py-8">Cargando períodos...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Períodos Académicos</h1>
        <button onClick={openCreateModal} className="btn-primary">
          + Nuevo Período
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {periods.map((period) => (
          <div key={period.id} className="card">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{period.name}</h3>
                <p className="text-sm text-gray-500 mt-1">
                  Inicio: {new Date(period.start_date).toLocaleDateString()}
                </p>
                <p className="text-sm text-gray-500">
                  Fin: {new Date(period.end_date).toLocaleDateString()}
                </p>
                {period.is_active && (
                  <span className="inline-block mt-2 px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                    Activo
                  </span>
                )}
              </div>
              <div className="space-x-2">
                <button onClick={() => openEditModal(period)} className="text-blue-600 hover:text-blue-900">
                  Editar
                </button>
                <button onClick={() => handleDelete(period.id)} className="text-red-600 hover:text-red-900">
                  Eliminar
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {editingPeriod ? 'Editar Período' : 'Nuevo Período'}
              </h3>
              <button onClick={() => setShowModal(false)} className="text-gray-400 hover:text-gray-600">✕</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Nombre</label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Fecha Inicio</label>
                  <input
                    type="datetime-local"
                    required
                    value={formData.start_date}
                    onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Fecha Fin</label>
                  <input
                    type="datetime-local"
                    required
                    value={formData.end_date}
                    onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="mt-6 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowModal(false)} className="btn-danger">Cancelar</button>
                <button type="submit" className="btn-primary">{editingPeriod ? 'Actualizar' : 'Crear'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Periods;