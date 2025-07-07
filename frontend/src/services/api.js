import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          throw new Error(data.detail || 'Bad request');
        case 401:
          throw new Error('Unauthorized');
        case 403:
          throw new Error('Forbidden');
        case 404:
          throw new Error('Not found');
        case 422:
          throw new Error(data.detail || 'Validation error');
        case 500:
          throw new Error('Internal server error');
        default:
          throw new Error(data.detail || `Server error: ${status}`);
      }
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error: Unable to connect to server');
    } else {
      // Something else happened
      throw new Error(error.message || 'Unknown error occurred');
    }
  }
);

// API functions
export const checkCompliance = async (concern, context = null) => {
  try {
    const response = await api.post('/api/v1/compliance/check', {
      concern,
      context,
    });
    return response.data;
  } catch (error) {
    console.error('Error checking compliance:', error);
    throw error;
  }
};

export const getDocumentStatus = async () => {
  try {
    const response = await api.get('/api/v1/documents/status');
    return response.data;
  } catch (error) {
    console.error('Error fetching document status:', error);
    throw error;
  }
};

export const reloadDocuments = async () => {
  try {
    const response = await api.post('/api/v1/documents/reload');
    return response.data;
  } catch (error) {
    console.error('Error reloading documents:', error);
    throw error;
  }
};

export const getHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

export const getApiInfo = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    console.error('Error fetching API info:', error);
    throw error;
  }
};

// Export the api instance for custom requests
export default api; 