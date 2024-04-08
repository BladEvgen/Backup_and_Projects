import { ReactNode } from "react";
import { createBrowserRouter } from "react-router-dom";
import MainPage from "./pages/MainPage";
interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return <div>{children}</div>;
};

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout>{<MainPage />}</Layout>,
  },
]);

export default router;
