import { Fragment } from "react/jsx-runtime";
import Header from "./components/Header";
import AppMain from "./components/layout/AppMain";
import { AppRouter } from "./router/router";
import { AuthProvider } from "./contexts/auth";

function App() {
  return (
    <Fragment>
      <AuthProvider>
        <Header />
        <AppMain>
          <AppRouter />
        </AppMain>
      </AuthProvider>
    </Fragment>
  );
}

export default App;
