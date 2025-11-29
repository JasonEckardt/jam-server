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
  refetch: () => { },
};

const AuthProviderContext = createContext<AuthProviderState>(initialState);

export function AuthProvider({ children, ...props }: AuthProviderProps) {
  const hasFetchedRef = useRef(false);

  const { data, isLoading, isError, isFetchedAfterMount, refetch } = useQuery<any, Error>({
    queryKey: ["me"],
    queryFn: () => fetch("/me"),
    refetchOnMount: false,
    refetchOnWindowFocus: false,
    retry: false,
    staleTime: 5 * 60 * 1000, // Cache for 5 min to avoid repeated calls
  });

  // Mark as fetched after first success or error
  useEffect(() => {
    if ((isFetchedAfterMount || isError) && !hasFetchedRef.current) {
      hasFetchedRef.current = true;
    }
  }, [isFetchedAfterMount, isError]);

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
