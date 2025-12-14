import { AppRouter } from "./router/router";
import { AuthProvider } from "./contexts/auth";

function App() {
  return (
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  );
}

export default App;
