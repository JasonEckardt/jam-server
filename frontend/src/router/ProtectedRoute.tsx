import { useAuth } from "@/contexts/auth";
import { Navigate, Outlet } from "react-router-dom";

export const ProtectedRoute = () => {
  const { isLogged } = useAuth();

  // TODO: Check for initialized when we start handling auth state like for user /me

  return isLogged ? <Outlet /> : <Navigate to="/login" replace />;
};
