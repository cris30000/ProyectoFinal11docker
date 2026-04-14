import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Users from './pages/Users';
import Periods from './pages/Periods';
import Grades from './pages/Grades';
import StudentGrades from './pages/StudentGrades';  // ✅ IMPORTAR

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="users" element={<Users />} />
            <Route path="periods" element={<Periods />} />
            <Route path="grades" element={<Grades />} />
            <Route path="my-grades" element={<StudentGrades />} />  {/* ✅ AGREGAR ESTA LÍNEA */}
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;