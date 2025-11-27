import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ProtectedRoute } from "./ProtectedRoute";
import { PublicRoute } from "./PublicRoute";
import { Layout } from "@/components/layout/AppMain"
import LibraryPage from "@/pages/library"
import Login from "@/components/Login";
import MainPage from "@/pages";
import NotFoundPage from "@/pages/notfound";
import UserPage from "@/pages/user";

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <MainPage /> },
      {
        element: <PublicRoute />,
        children: [
          { path: "/login", element: <Login /> },
        ],
      },
      {
        element: <ProtectedRoute />,
        children: [
          { path: "/me", element: <UserPage /> },
          { path: "/library", element: <LibraryPage /> },
        ],
      },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);

export const AppRouter = () => <RouterProvider router={router} />;
