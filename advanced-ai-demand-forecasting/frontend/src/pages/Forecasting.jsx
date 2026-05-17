import { useEffect, useState } from "react";
import api from "../api/axios";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";

export default function Forecasting() {
  const [datasets, setDatasets] = useState([]);
  const [history, setHistory] = useState([]);
  const [result, setResult] = useState(null);

  const [form, setForm] = useState({
    dataset_id: "",
    target_column: "sales",
    date_column: "date",
    model_name: "linear_regression",
    forecast_periods: 7,
  });

  const load = async () => {
    const ds = await api.get("/datasets/");
    setDatasets(ds.data.data.items);

    const h = await api.get("/forecasts/history");
    setHistory(h.data.data.items);
  };

  useEffect(() => {
    load();
  }, []);

  const generate = async (e) => {
    e.preventDefault();

    const res = await api.post("/forecasts/generate", {
      ...form,
      dataset_id: Number(form.dataset_id),
      forecast_periods: Number(form.forecast_periods),
    });

    setResult(res.data.data);
    load();
  };

  const compare = async () => {
    const res = await api.post("/forecasts/compare", {
      dataset_id: Number(form.dataset_id),
      target_column: form.target_column,
      date_column: form.date_column,
      forecast_periods: Number(form.forecast_periods),
    });

    setResult(res.data.data);
    load();
  };

  return (
    <div className="page">
      <h2>Forecasting</h2>

      <form className="card" onSubmit={generate}>
        <h3>Generate Forecast</h3>

        <div className="grid grid-2">
          <select onChange={(e) => setForm({ ...form, dataset_id: e.target.value })}>
            <option value="">Select Dataset</option>
            {datasets.map((d) => (
              <option value={d.id} key={d.id}>{d.name}</option>
            ))}
          </select>

          <input value={form.target_column} placeholder="Target Column" onChange={(e) => setForm({ ...form, target_column: e.target.value })} />
          <input value={form.date_column} placeholder="Date Column" onChange={(e) => setForm({ ...form, date_column: e.target.value })} />

          <select value={form.model_name} onChange={(e) => setForm({ ...form, model_name: e.target.value })}>
            <option value="linear_regression">Linear Regression</option>
            <option value="random_forest">Random Forest</option>
            <option value="arima">ARIMA</option>
            <option value="moving_average">Moving Average</option>
          </select>

          <input type="number" value={form.forecast_periods} onChange={(e) => setForm({ ...form, forecast_periods: e.target.value })} />
        </div>

        <br />
        <button className="btn">Generate</button>{" "}
        <button type="button" className="btn btn-secondary" onClick={compare}>Compare Models</button>
      </form>

      {result && (
        <div className="card">
          <h3>Forecast Result</h3>
          <p>Model: {result.model_name}</p>
          <p>MAE: {result.mae} | RMSE: {result.rmse} | MAPE: {result.mape}</p>

          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={result.predictions || []}>
              <XAxis dataKey="period" />
              <YAxis />
              <Tooltip />
              <Line dataKey="predicted_value" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="card">
        <h3>Forecast History</h3>

        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Dataset</th>
              <th>Model</th>
              <th>Target</th>
              <th>RMSE</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h) => (
              <tr key={h.id}>
                <td>{h.id}</td>
                <td>{h.dataset_id}</td>
                <td>{h.model_name}</td>
                <td>{h.target_column}</td>
                <td>{h.rmse}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}