import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.js";
import "@/css/index.css";

import queryClient from "./services/queryClient.js";
import { QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "./contexts/theme.js";
import { AuthProvider } from "./contexts/auth.js";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <AuthProvider>
          <App />
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  </StrictMode>,
);
