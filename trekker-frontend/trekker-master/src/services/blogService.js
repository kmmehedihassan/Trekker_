import api from './api';

export const blogService = {
  // Get all categories
  getCategories: async () => {
    const response = await api.get('/categories/');
    return response.data;
  },

  // Get all posts
  getAllPosts: async (params = {}) => {
    const response = await api.get('/posts/', { params });
    return response.data;
  },

  // Get single post
  getPost: async (slug) => {
    const response = await api.get(`/posts/${slug}/`);
    return response.data;
  },

  // Search posts
  searchPosts: async (query) => {
    const response = await api.get('/posts/search/', { params: { q: query } });
    return response.data;
  },

  // Create post
  createPost: async (postData) => {
    const response = await api.post('/posts/', postData);
    return response.data;
  },

  // Update post
  updatePost: async (slug, postData) => {
    const response = await api.put(`/posts/${slug}/`, postData);
    return response.data;
  },

  // Delete post
  deletePost: async (slug) => {
    const response = await api.delete(`/posts/${slug}/`);
    return response.data;
  },

  // Like/Unlike post
  likePost: async (slug) => {
    const response = await api.post(`/posts/${slug}/like/`);
    return response.data;
  },

  // Get user's posts
  getMyPosts: async () => {
    const response = await api.get('/posts/my_posts/');
    return response.data;
  },

  // Get comments for post
  getComments: async (postSlug) => {
    const response = await api.get('/comments/', { params: { post: postSlug } });
    return response.data;
  },

  // Create comment
  createComment: async (commentData) => {
    const response = await api.post('/comments/', commentData);
    return response.data;
  },
};

export default blogService;
