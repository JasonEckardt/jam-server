import { api } from "@/services/api";

type FetchOptions<P = any> = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  params?: P;
  body?: P;
  headers?: Record<string, string>;
};

export async function fetch<P = any, R = any>(
  endpoint: string,
  { method = "GET", params, body, headers }: FetchOptions<P> = {},
): Promise<R> {
  const config = {
    url: endpoint,
    method,
    params: method === "GET" ? params : undefined,
    data: method !== "GET" ? body : undefined,
    headers,
    withCredentials: true,
  };

  const { data } = await api.request<R>(config);
  return data;
}
