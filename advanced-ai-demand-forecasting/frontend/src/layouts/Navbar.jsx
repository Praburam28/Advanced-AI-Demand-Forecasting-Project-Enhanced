import { LogOut, UserCircle } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav
      style={{
        height: 76,
        background: "rgba(255,255,255,0.85)",
        backdropFilter: "blur(14px)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "0 28px",
        boxShadow: "0 8px 28px rgba(99,102,241,0.12)",
        position: "sticky",
        top: 0,
        zIndex: 10,
      }}
    >
      <div>
        <h3 style={{ margin: 0, fontSize: 22 }}>Advanced AI Demand Forecasting</h3>
        <small style={{ color: "#6b7280" }}>Forecast smarter. Plan faster.</small>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <UserCircle color="#7c3aed" />
        <div>
          <strong>{user?.name}</strong>
          <br />
          <small>{user?.role}</small>
        </div>

        <button className="btn btn-danger" onClick={logout}>
          <LogOut size={16} style={{ verticalAlign: "middle" }} /> Logout
        </button>
      </div>
    </nav>
  );
}