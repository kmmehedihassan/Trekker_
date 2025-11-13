import api from './api';
import axios from 'axios';

const AUTH_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

export const authService = {
  // Register new user
  register: async (userData) => {
    const response = await axios.post(`${AUTH_BASE_URL}/auth/register/`, userData);
    if (response.data.tokens) {
      localStorage.setItem('access_token', response.data.tokens.access);
      localStorage.setItem('refresh_token', response.data.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  // Login user
  login: async (username, password) => {
    const response = await axios.post(`${AUTH_BASE_URL}/auth/login/`, {
      username,
      password,
    });
    if (response.data.tokens) {
      localStorage.setItem('access_token', response.data.tokens.access);
      localStorage.setItem('refresh_token', response.data.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  // Logout user
  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    try {
      await api.post('/auth/logout/', { refresh_token: refreshToken });
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  // Get current user profile
  getCurrentUser: async () => {
    const response = await api.get('/users/me/');
    return response.data;
  },

  // Update user profile
  updateProfile: async (profileData) => {
    const response = await api.put('/users/update_profile/', profileData);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  },

  // Upload profile picture
  uploadProfilePicture: async (formData) => {
    const response = await api.post('/users/upload_profile_picture/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  },

  // Change password
  changePassword: async (oldPassword, newPassword) => {
    const response = await api.post('/users/change_password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password2: newPassword,
    });
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },

  // Get stored user data
  getStoredUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

export default authService;
