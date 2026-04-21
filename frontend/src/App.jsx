import Dashboard from "./components/Dashboard";
import Predict from "./components/Predict";
import Insights from "./components/Insights";

function App() {
  return (
    <div style={{ padding: "40px", maxWidth: "900px", margin: "auto" }}>
      <h1 style={{ textAlign: "center" }}>Traffic Analysis System</h1>

      <Dashboard />
      <Predict />
      <Insights />
    </div>
  );
}

export default App;