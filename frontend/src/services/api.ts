import type { AxiosInstance, AxiosRequestConfig } from "axios";
import axios, { AxiosError } from "axios";

export const api: AxiosInstance = axios.create({
  baseURL: "/api",
});

api.interceptors.request.use((config) => {
  // Configs used in every request
  config.headers.set("Accept", "application/json");

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
    }

    return Promise.reject(error);
  },
);
