import { useEffect, useState } from "react";
import api from "../api/axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import { Database, LineChart as LineIcon, Target, Percent } from "lucide-react";

export default function Dashboard() {
  const [summary, setSummary] = useState({});
  const [analytics, setAnalytics] = useState({});

  useEffect(() => {
    api.get("/dashboard/summary").then((res) => setSummary(res.data.data));
    api.get("/dashboard/analytics").then((res) => setAnalytics(res.data.data));
  }, []);

  return (
    <div className="page">
      <h2>Dashboard Overview</h2>

      <div className="grid grid-4">
        <div className="card stat-card stat-blue">
          <h3>Total Datasets</h3>
          <h1>{summary.total_datasets || 0}</h1>
          <Database size={70} className="stat-icon" />
        </div>

        <div className="card stat-card stat-purple">
          <h3>Total Forecasts</h3>
          <h1>{summary.total_forecasts || 0}</h1>
          <LineIcon size={70} className="stat-icon" />
        </div>

        <div className="card stat-card stat-green">
          <h3>Average RMSE</h3>
          <h1>{summary.average_rmse || 0}</h1>
          <Target size={70} className="stat-icon" />
        </div>

        <div className="card stat-card stat-orange">
          <h3>Average MAPE</h3>
          <h1>{summary.average_mape || 0}%</h1>
          <Percent size={70} className="stat-icon" />
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h3>Forecast Activity</h3>
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={analytics.forecast_activity || []}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="forecast_count" strokeWidth={4} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3>Model Usage</h3>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={analytics.model_usage || []}>
              <XAxis dataKey="model_name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" radius={[12, 12, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h3>Model Performance</h3>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={analytics.model_performance || []}>
            <XAxis dataKey="model_name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="average_rmse" radius={[12, 12, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}