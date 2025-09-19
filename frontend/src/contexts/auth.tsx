import { fetch } from "@/services/fetch";
import { useQuery } from "@tanstack/react-query";
import type { ReactNode } from "react";
import { createContext, useContext, useRef, useEffect } from "react";

type AuthProviderProps = {
  children: ReactNode;
};

type AuthProviderState = {
  data: any;
  isLogged: boolean;
  isInitialized: boolean;
  isLoading: boolean;
  refetch: () => void;
};

const initialState: AuthProviderState = {
  data: null,
  isLogged: false,
  isInitialized: false,
  isLoading: false,
  refetch: () => {},
};

const AuthProviderContext = createContext<AuthProviderState>(initialState);

export function AuthProvider({ children, ...props }: AuthProviderProps) {
  const location = window.location;
  const hasFetchedRef = useRef(false);

  // Only enable the query if on /me and we haven't fetched yet
  const shouldFetch = location.pathname === "/me" && !hasFetchedRef.current;

  const { data, isLoading, isError, isFetchedAfterMount, refetch } = useQuery<any, Error>({
    queryKey: ["me"],
    queryFn: () => fetch("/me"),
    enabled: shouldFetch,
    retry: false,
  });

  // Mark as fetched after first success or error
  useEffect(() => {
    if ((isFetchedAfterMount || isError) && !hasFetchedRef.current) {
      hasFetchedRef.current = true;
    }
  }, [isFetchedAfterMount, isError]);

  console.log(data, isLoading, isFetchedAfterMount);

  const isLogged = !!data && !isError;

  const value = { data, isLogged, isInitialized: isFetchedAfterMount, isLoading, refetch };

  return (
    <AuthProviderContext.Provider {...props} value={value}>
      {children}
    </AuthProviderContext.Provider>
  );
}
// ...existing code...

export const useAuth = () => {
  const context = useContext(AuthProviderContext);

  if (context === undefined) throw new Error("useAuth must be used within a AuthProvider");

  return context;
};
