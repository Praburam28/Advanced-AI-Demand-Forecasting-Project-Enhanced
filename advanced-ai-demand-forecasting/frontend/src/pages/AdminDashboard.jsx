import { useEffect, useState } from "react";
import api from "../api/axios";

export default function AdminDashboard() {
  const [overview, setOverview] = useState(null);
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const overviewRes = await api.get("/admin/overview");
      setOverview(overviewRes.data.data);

      const usersRes = await api.get("/admin/users");
      setUsers(usersRes.data.data.items);
    } catch {
      setError("Admin access required. Please update user role to admin and login again.");
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (error) {
    return (
      <div className="page">
        <h2>Admin Panel</h2>
        <div className="card">
          <p className="error">{error}</p>
          <p>Run this in MySQL:</p>
          <pre>
{`UPDATE users SET role='admin' WHERE email='your_email@gmail.com';`}
          </pre>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <h2>Admin Panel</h2>

      {overview && (
        <div className="grid grid-4">
          <div className="card"><h3>Users</h3><h1>{overview.total_users}</h1></div>
          <div className="card"><h3>Active Users</h3><h1>{overview.active_users}</h1></div>
          <div className="card"><h3>Datasets</h3><h1>{overview.total_datasets}</h1></div>
          <div className="card"><h3>Forecasts</h3><h1>{overview.total_forecasts}</h1></div>
        </div>
      )}

      <div className="card">
        <h3>Users</h3>

        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Active</th>
            </tr>
          </thead>

          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.name}</td>
                <td>{u.email}</td>
                <td>{u.role}</td>
                <td>{u.is_active ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}