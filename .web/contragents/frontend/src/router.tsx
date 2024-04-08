import { ReactNode } from "react";
import { createBrowserRouter } from "react-router-dom";

import MainPage from "./pages/MainPage.tsx";
import StaffPage from "./pages/StaffPage.tsx";
import RegisterPage from "./pages/RegisterPage.tsx";
import HeaderComponent from "./components/HeaderComponent.tsx";
import LoginPage from "./pages/LoginPage.tsx";

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div>
      <HeaderComponent />
      {children}
    </div>
  );
};

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout>{status ? <StaffPage /> : <MainPage />}</Layout>,
  },
  {
    path: "/register",
    element: (
      <Layout>
        <RegisterPage />
      </Layout>
    ),
  },
  {
    path: "/login",
    element: (
      <Layout>
        <LoginPage />
      </Layout>
    ),
  },
]);

export default router;
