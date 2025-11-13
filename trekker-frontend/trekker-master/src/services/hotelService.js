import api from './api';

export const hotelService = {
  // Get all hotels
  getAllHotels: async (params = {}) => {
    const response = await api.get('/hotels/', { params });
    return response.data;
  },

  // Get single hotel
  getHotel: async (id) => {
    const response = await api.get(`/hotels/${id}/`);
    return response.data;
  },

  // Get hotel rooms
  getHotelRooms: async (hotelId) => {
    const response = await api.get(`/hotels/${hotelId}/rooms/`);
    return response.data;
  },

  // Search hotels
  searchHotels: async (query) => {
    const response = await api.get('/hotels/search/', { params: { q: query } });
    return response.data;
  },

  // Get all rooms
  getRooms: async (params = {}) => {
    const response = await api.get('/rooms/', { params });
    return response.data;
  },

  // Create hotel reservation
  createReservation: async (reservationData) => {
    const response = await api.post('/hotel-reservations/', reservationData);
    return response.data;
  },

  // Get user reservations
  getMyReservations: async () => {
    const response = await api.get('/hotel-reservations/my_reservations/');
    return response.data;
  },

  // Cancel reservation
  cancelReservation: async (id) => {
    const response = await api.post(`/hotel-reservations/${id}/cancel/`);
    return response.data;
  },
};

export default hotelService;
