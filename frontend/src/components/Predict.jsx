import { useState } from "react";
import axios from "axios";

function Predict() {
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    const data = {
      hour: 18,
      day_of_week: 2,
      month: 10,
      temp: 290,
      rain_1h: 0,
      snow_1h: 0,
      clouds_all: 40,
      holiday: 0,
      weather_main_Clear: 1
    };

    const res = await axios.post("http://127.0.0.1:5000/predict", data);
    setResult(res.data.prediction);
  };

  return (
    <div>
      <h2>Prediction</h2>
      <button onClick={handlePredict}>Predict Traffic</button>

      {result && <p>Prediction: {result}</p>}
    </div>
  );
}

export default Predict;