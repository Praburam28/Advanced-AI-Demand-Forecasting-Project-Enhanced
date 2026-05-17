import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [form, setForm] = useState({
    file: null,
    name: "",
    product_category: "",
    region: "",
  });

  const loadDatasets = async () => {
    const res = await api.get("/datasets/");
    setDatasets(res.data.data.items);
  };

  useEffect(() => {
    loadDatasets();
  }, []);

  const upload = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append("file", form.file);
    data.append("name", form.name);
    data.append("product_category", form.product_category);
    data.append("region", form.region);

    await api.post("/datasets/upload", data);
    alert("Dataset uploaded successfully");
    loadDatasets();
  };

  return (
    <div className="page">
      <h2>Datasets</h2>

      <form className="card" onSubmit={upload}>
        <h3>Upload Dataset</h3>

        <div className="grid grid-2">
          <input type="file" accept=".csv,.xlsx,.xls" onChange={(e) => setForm({ ...form, file: e.target.files[0] })} />
          <input placeholder="Dataset Name" onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Product Category" onChange={(e) => setForm({ ...form, product_category: e.target.value })} />
          <input placeholder="Region" onChange={(e) => setForm({ ...form, region: e.target.value })} />
        </div>

        <br />
        <button className="btn">Upload</button>
      </form>

      <div className="card">
        <h3>Uploaded Datasets</h3>

        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Rows</th>
              <th>Columns</th>
              <th>Category</th>
              <th>Region</th>
            </tr>
          </thead>
          <tbody>
            {datasets.map((d) => (
              <tr key={d.id}>
                <td>{d.id}</td>
                <td>{d.name}</td>
                <td>{d.total_rows}</td>
                <td>{d.total_columns}</td>
                <td>{d.product_category}</td>
                <td>{d.region}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}