import { useAuth } from "@/contexts/auth";
import { Navigate, Outlet } from "react-router-dom";

export const PublicRoute = () => {
  const { isLoggedIn } = useAuth();

  return !isLoggedIn ? <Outlet /> : <Navigate to="/" replace />;
};
