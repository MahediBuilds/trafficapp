import { useEffect, useState } from "react";
import axios from "axios";

function Insights() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/insights")
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div>
      <h2>Insights</h2>
      <p>Peak Hour: {data.peak_hour}</p>
      <p>Average Traffic: {data.average_traffic}</p>

      <p>
        Insight: Traffic is highest around {data.peak_hour}:00 hours.
      </p>
    </div>
  );
}

export default Insights;