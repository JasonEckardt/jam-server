import { useAuth } from "@/contexts/auth";
import { Navigate, Outlet } from "react-router-dom";

export const PublicRoute = () => {
  const { isLogged } = useAuth();

  return !isLogged ? <Outlet /> : <Navigate to="/" replace />;
};
