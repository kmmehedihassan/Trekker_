import api from './api';

export const tourService = {
  // Get all tours
  getAllTours: async (params = {}) => {
    const response = await api.get('/tours/', { params });
    return response.data;
  },

  // Get single tour
  getTour: async (id) => {
    const response = await api.get(`/tours/${id}/`);
    return response.data;
  },

  // Search tours
  searchTours: async (query) => {
    const response = await api.get('/tours/search/', { params: { q: query } });
    return response.data;
  },

  // Create tour booking
  createBooking: async (bookingData) => {
    const response = await api.post('/tour-bookings/', bookingData);
    return response.data;
  },

  // Get user bookings
  getMyBookings: async () => {
    const response = await api.get('/tour-bookings/my_bookings/');
    return response.data;
  },

  // Cancel booking
  cancelBooking: async (id) => {
    const response = await api.post(`/tour-bookings/${id}/cancel/`);
    return response.data;
  },
};

export default tourService;
