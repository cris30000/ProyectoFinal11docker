import api from './api';

export const authService = {
  async login(username, password) {
    const response = await api.post('/auth/login', { username, password });
    if (response.data.user) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
      localStorage.setItem('token', 'fake-token');
    }
    return response.data;
  },

  logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  },

  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
};