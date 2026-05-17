import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [forecastId, setForecastId] = useState("");
  const [reportType, setReportType] = useState("pdf");

  const loadReports = async () => {
    const res = await api.get("/reports/");
    setReports(res.data.data.items);
  };

  useEffect(() => {
    loadReports();
  }, []);

  const generate = async (e) => {
    e.preventDefault();

    await api.post("/reports/generate", {
      forecast_id: Number(forecastId),
      report_type: reportType,
    });

    alert("Report generated");
    loadReports();
  };

  const download = async (id) => {
    const res = await api.get(`/reports/${id}/download`, {
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.download = `report_${id}`;
    link.click();
  };

  return (
    <div className="page">
      <h2>Reports</h2>

      <form className="card" onSubmit={generate}>
        <h3>Generate Report</h3>

        <div className="grid grid-2">
          <input placeholder="Forecast ID" value={forecastId} onChange={(e) => setForecastId(e.target.value)} />

          <select value={reportType} onChange={(e) => setReportType(e.target.value)}>
            <option value="summary">Summary</option>
            <option value="pdf">PDF</option>
            <option value="excel">Excel</option>
          </select>
        </div>

        <br />
        <button className="btn">Generate Report</button>
      </form>

      <div className="card">
        <h3>Reports List</h3>

        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Forecast ID</th>
              <th>Type</th>
              <th>Download</th>
            </tr>
          </thead>

          <tbody>
            {reports.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.forecast_id}</td>
                <td>{r.report_type}</td>
                <td>
                  {r.report_type === "pdf" || r.report_type === "excel" ? (
                    <button className="btn" onClick={() => download(r.id)}>Download</button>
                  ) : (
                    "View Only"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}