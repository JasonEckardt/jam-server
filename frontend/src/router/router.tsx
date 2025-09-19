import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ProtectedRoute } from "./ProtectedRoute";
import { PublicRoute } from "./PublicRoute";
import Login from "@/components/Login";
import UserPage from "@/pages/user";
import MainPage from "@/pages";

const router = createBrowserRouter([
  {
    element: <PublicRoute />,
    children: [{ path: "/login", element: <Login /> }],
  },
  {
    element: <ProtectedRoute />,
    children: [
      { path: "/", element: <MainPage /> },
      { path: "/me", element: <UserPage /> },
    ],
  },
  // { path: "*", element: <NotFoundRoute /> },
]);

export const AppRouter = () => <RouterProvider router={router} />;
