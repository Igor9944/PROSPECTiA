import axios from "axios";

const appBase = (import.meta.env.BASE_URL || "/").replace(/\/$/, "");
const apiBase = import.meta.env.VITE_API_URL || "/api";

const api = axios.create({
  baseURL: apiBase,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      const loginPath = `${appBase}/login`;
      if (!window.location.pathname.startsWith(loginPath) && !window.location.pathname.endsWith("/login")) {
        window.location.href = loginPath;
      }
    }
    return Promise.reject(error);
  }
);

export default api;
