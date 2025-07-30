import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 认证相关API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
};

// 项目管理API
export const projectsAPI = {
  getProjects: (params) => api.get('/projects', { params }),
  getProject: (id) => api.get(`/projects/${id}`),
  createProject: (data) => api.post('/projects', data),
  updateProject: (id, data) => api.put(`/projects/${id}`, data),
  deleteProject: (id) => api.delete(`/projects/${id}`),
  addUserToProject: (projectId, userId, role) => 
    api.post(`/projects/${projectId}/users/${userId}`, { role }),
};

// 媒体文件API
export const mediaAPI = {
  getMediaFiles: (params) => api.get('/media', { params }),
  getMediaFile: (id) => api.get(`/media/${id}`),
  uploadMediaFile: (file, projectId) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('project_id', projectId);
    return api.post('/media/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  deleteMediaFile: (id) => api.delete(`/media/${id}`),
};

// 标注API
export const annotationsAPI = {
  getAnnotations: (params) => api.get('/annotations', { params }),
  getAnnotation: (id) => api.get(`/annotations/${id}`),
  createAnnotation: (data) => api.post('/annotations', data),
  updateAnnotation: (id, data) => api.put(`/annotations/${id}`, data),
  deleteAnnotation: (id) => api.delete(`/annotations/${id}`),
  reviewAnnotation: (id, status, comment) => 
    api.post(`/annotations/review/${id}`, { status, comment }),
};

// 标签API
export const labelsAPI = {
  getLabels: (projectId) => api.get(`/projects/${projectId}/labels`),
  createLabel: (projectId, data) => api.post(`/projects/${projectId}/labels`, data),
  updateLabel: (id, data) => api.put(`/labels/${id}`, data),
  deleteLabel: (id) => api.delete(`/labels/${id}`),
};

// 用户管理API
export const usersAPI = {
  getUsers: (params) => api.get('/users', { params }),
  getUser: (id) => api.get(`/users/${id}`),
  createUser: (data) => api.post('/users', data),
  updateUser: (id, data) => api.put(`/users/${id}`, data),
  deleteUser: (id) => api.delete(`/users/${id}`),
};

// 统计API
export const statsAPI = {
  getProjectStats: (projectId) => api.get(`/projects/${projectId}/stats`),
  getAnnotationStats: (projectId) => api.get(`/projects/${projectId}/annotation-stats`),
  exportAnnotations: (projectId, format) => 
    api.get(`/projects/${projectId}/export`, { params: { format } }),
};

export default api;