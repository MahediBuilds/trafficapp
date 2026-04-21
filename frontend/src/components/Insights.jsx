import { useEffect, useState } from "react";
import axios from "axios";

function Insights() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/insights")
      .then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h2>Insights</h2>
      {data && (
        <>
          <p>Peak Hour: {data.peak_hour}</p>
          <p>Average Traffic: {data.average_traffic}</p>
        </>
      )}
    </div>
  );
}

export default Insights;