import { useAuth } from "@/contexts/auth";
import { Navigate, Outlet } from "react-router-dom";

export const ProtectedRoute = () => {
  const { isLogged, isInitialized } = useAuth();

  console.log(isLogged, isInitialized);

  if (!isInitialized) return null; // or a loading spinner

  return isLogged ? <Outlet /> : <Navigate to="/login" replace />;
};
