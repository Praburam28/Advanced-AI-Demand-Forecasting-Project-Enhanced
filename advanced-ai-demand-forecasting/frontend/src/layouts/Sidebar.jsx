import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Database,
  LineChart,
  FileText,
  Bell,
  Shield,
  Sparkles,
} from "lucide-react";

export default function Sidebar() {
  const links = [
    { path: "/dashboard", label: "Dashboard", icon: <LayoutDashboard size={20} /> },
    { path: "/datasets", label: "Datasets", icon: <Database size={20} /> },
    { path: "/forecasting", label: "Forecasting", icon: <LineChart size={20} /> },
    { path: "/reports", label: "Reports", icon: <FileText size={20} /> },
    { path: "/notifications", label: "Notifications", icon: <Bell size={20} /> },
    { path: "/admin", label: "Admin Panel", icon: <Shield size={20} /> },
  ];

  return (
    <aside
      style={{
        width: 270,
        minHeight: "100vh",
        padding: 22,
        background: "linear-gradient(180deg, #111827, #312e81, #581c87)",
        color: "white",
        position: "sticky",
        top: 0,
      }}
    >
      <div
        style={{
          display: "flex",
          gap: 12,
          alignItems: "center",
          marginBottom: 34,
        }}
      >
        <div
          style={{
            width: 46,
            height: 46,
            borderRadius: 16,
            background: "linear-gradient(135deg, #38bdf8, #a78bfa, #f472b6)",
            display: "grid",
            placeItems: "center",
          }}
        >
          <Sparkles size={25} />
        </div>

        <div>
          <h2 style={{ margin: 0, fontSize: 22 }}>AI Forecast</h2>
          <small style={{ opacity: 0.75 }}>Demand Intelligence</small>
        </div>
      </div>

      {links.map((link) => (
        <NavLink
          key={link.path}
          to={link.path}
          style={({ isActive }) => ({
            display: "flex",
            gap: 12,
            alignItems: "center",
            color: "white",
            padding: "13px 14px",
            borderRadius: 16,
            marginBottom: 10,
            fontWeight: 700,
            background: isActive
              ? "linear-gradient(135deg, #2563eb, #db2777)"
              : "rgba(255,255,255,0.08)",
            boxShadow: isActive
              ? "0 12px 28px rgba(219,39,119,0.35)"
              : "none",
          })}
        >
          {link.icon}
          {link.label}
        </NavLink>
      ))}
    </aside>
  );
}