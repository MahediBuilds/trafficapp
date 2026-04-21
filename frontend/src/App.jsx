import Dashboard from "./components/Dashboard";
import Predict from "./components/Predict";
import Insights from "./components/Insights";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Traffic Analysis System</h1>
      <Dashboard />
      <Predict />
      <Insights />
    </div>
  );
}

export default App;