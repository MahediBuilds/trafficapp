import { useEffect, useState } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/get-data")
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  if (data.length === 0) return <p>Loading...</p>;

  // Group by hour
  const grouped = {};
  data.forEach(d => {
    if (!grouped[d.hour]) grouped[d.hour] = [];
    grouped[d.hour].push(d.traffic_volume);
  });

  const hours = Object.keys(grouped);
  const avgTraffic = hours.map(h => {
    const arr = grouped[h];
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  });

  const chartData = {
    labels: hours,
    datasets: [
      {
        label: "Avg Traffic by Hour",
        data: avgTraffic,
        borderColor: "cyan",
        tension: 0.3
      }
    ]
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <Line data={chartData} />
    </div>
  );
}

export default Dashboard;