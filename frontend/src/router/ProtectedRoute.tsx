import { useAuth } from "@/contexts/auth";
import { Navigate, Outlet } from "react-router-dom";

export const ProtectedRoute = () => {
  const { isLogged, isInitialized } = useAuth();

  if (isInitialized) {
    return <div>Loading...</div>
  }

  return isLogged ? <Outlet /> : <Navigate to="/login" replace />;
};
