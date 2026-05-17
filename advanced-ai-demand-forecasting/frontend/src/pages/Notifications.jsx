import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);

  const load = async () => {
    const res = await api.get("/notifications/");
    setNotifications(res.data.data.items);
  };

  useEffect(() => {
    load();
  }, []);

  const markRead = async (id) => {
    await api.put(`/notifications/${id}/read`);
    load();
  };

  const markAll = async () => {
    await api.put("/notifications/read-all");
    load();
  };

  return (
    <div className="page">
      <h2>Notifications</h2>

      <button className="btn" onClick={markAll}>Mark All Read</button>
      <br /><br />

      {notifications.map((n) => (
        <div className="card" key={n.id}>
          <h3>{n.title}</h3>
          <p>{n.message}</p>
          <p>Type: {n.type}</p>
          <p>Status: {n.is_read ? "Read" : "Unread"}</p>

          {!n.is_read && (
            <button className="btn" onClick={() => markRead(n.id)}>Mark Read</button>
          )}
        </div>
      ))}
    </div>
  );
}