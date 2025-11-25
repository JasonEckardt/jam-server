import { useAuth } from "@/contexts/auth";
import { Navigate, Outlet } from "react-router-dom";

export const ProtectedRoute = () => {
  const { isLoggedIn, isLoading } = useAuth();

  // TODO: Check for initialized when we start handling auth state like for user /me
  if (isLoading) {
    return <div>Loading session...</div>;
  }


  return isLoggedIn ? <Outlet /> : <Navigate to="/login" replace />;
};
