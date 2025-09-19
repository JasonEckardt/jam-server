import type { AxiosInstance, AxiosRequestConfig } from "axios";
import axios, { AxiosError } from "axios";

export const api: AxiosInstance = axios.create({
  baseURL: "/api",
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      // Implement token refresh logic here if needed
    }

    return Promise.reject(error);
  },
);
