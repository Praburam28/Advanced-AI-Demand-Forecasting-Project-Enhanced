import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

export default function MainLayout() {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar />
      <main style={{ flex: 1, minHeight: "100vh" }}>
        <Navbar />
        <Outlet />
      </main>
    </div>
  );
}