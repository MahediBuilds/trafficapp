import { useState } from "react";
import axios from "axios";

function Predict() {
  const [hour, setHour] = useState(12);
  const [result, setResult] = useState(null);
  const [level, setLevel] = useState("");

  const handlePredict = async () => {
    const data = {
      hour: Number(hour),
      day_of_week: 2,
      month: 10,
      temp: 290,
      rain_1h: 0,
      snow_1h: 0,
      clouds_all: 40,
      holiday: 0,
      weather_main_Clear: 1
    };

    try {
      const res1 = await axios.post("http://3.108.60.145:5000/predict", data);
      const res2 = await axios.post("http://3.108.60.145:5000/classify", data);

      setResult(res1.data.prediction);
      setLevel(res2.data.traffic_level);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Prediction</h2>

      <input
        type="number"
        value={hour}
        onChange={(e) => setHour(e.target.value)}
        placeholder="Enter hour (0-23)"
      />

      <button onClick={handlePredict}>Predict</button>

      {result && <p>Prediction: {result}</p>}
      {level && <p>Traffic Level: {level}</p>}
    </div>
  );
}

export default Predict;