import { Fragment } from "react/jsx-runtime";
import Header from "./components/Header";
import AppMain from "./components/layout/AppMain";
import { AppRouter } from "./router/router";

function App() {
  return (
    <Fragment>
      <Header />
      <AppMain>
        <AppRouter />
      </AppMain>
    </Fragment>
  );
}

export default App;
