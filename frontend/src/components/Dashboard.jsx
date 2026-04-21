import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/get-data")
      .then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Data loaded: {data.length} rows</p>
    </div>
  );
}

export default Dashboard;