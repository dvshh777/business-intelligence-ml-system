import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000/api/v1";

const initialForm = {
  industry: "Technology",
  region: "West",
  monthly_revenue: 15000,
  active_users: 250,
  support_tickets: 12,
  last_login_days_ago: 4,
  contract_value: 30000,
  tenure_months: 14,
};

function MetricCard({ label, value, accent }) {
  return (
    <div className="metric-card">
      <span className="metric-label">{label}</span>
      <strong className="metric-value" style={{ color: accent }}>
        {value}
      </strong>
    </div>
  );
}

export default function App() {
  const [summary, setSummary] = useState(null);
  const [metrics, setMetrics] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const loadDashboard = async () => {
    const [summaryRes, metricsRes] = await Promise.all([
      fetch(`${API_BASE}/dashboard/summary`),
      fetch(`${API_BASE}/dashboard/model-metrics`),
    ]);
    setSummary(await summaryRes.json());
    setMetrics((await metricsRes.json()).metrics || {});
  };

  useEffect(() => {
    loadDashboard().catch(() => {
      setMessage("Backend is not reachable yet. Start FastAPI and seed data.");
    });
  }, []);

  const handleTrain = async () => {
    setLoading(true);
    setMessage("");
    try {
      const response = await fetch(`${API_BASE}/ml/train`, { method: "POST" });
      const data = await response.json();
      setMetrics(data.metrics || {});
      await loadDashboard();
      setMessage("Model training completed successfully.");
    } catch {
      setMessage("Training failed. Make sure the database is seeded first.");
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const response = await fetch(`${API_BASE}/ml/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          monthly_revenue: Number(form.monthly_revenue),
          active_users: Number(form.active_users),
          support_tickets: Number(form.support_tickets),
          last_login_days_ago: Number(form.last_login_days_ago),
          contract_value: Number(form.contract_value),
          tenure_months: Number(form.tenure_months),
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed");
      }
      setPrediction(data);
      setMessage("Prediction generated.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Business Intelligence + Machine Learning</p>
          <h1>Customer risk, commercial signals, and model operations in one dashboard.</h1>
          <p className="hero-copy">
            This starter project tracks operational KPIs, retrains a churn classifier, and serves
            real-time risk predictions through a single API-backed React interface.
          </p>
        </div>
        <button className="primary-button" onClick={handleTrain} disabled={loading}>
          {loading ? "Working..." : "Retrain Model"}
        </button>
      </header>

      {message ? <div className="banner">{message}</div> : null}

      <section className="metrics-grid">
        <MetricCard label="Customers" value={summary?.total_customers ?? "--"} accent="#0f766e" />
        <MetricCard
          label="Monthly Revenue"
          value={summary ? `$${summary.monthly_revenue.toLocaleString()}` : "--"}
          accent="#b45309"
        />
        <MetricCard
          label="Avg Contract"
          value={summary ? `$${summary.avg_contract_value.toLocaleString()}` : "--"}
          accent="#1d4ed8"
        />
        <MetricCard
          label="Churn Rate"
          value={summary ? `${(summary.churn_rate * 100).toFixed(1)}%` : "--"}
          accent="#be123c"
        />
        <MetricCard
          label="Predicted At Risk"
          value={summary?.at_risk_customers ?? "--"}
          accent="#7c3aed"
        />
      </section>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-header">
            <h2>Model Metrics</h2>
            <span>Latest evaluation</span>
          </div>
          <div className="metric-list">
            {Object.keys(metrics).length ? (
              Object.entries(metrics).map(([key, value]) => (
                <div className="metric-row" key={key}>
                  <span>{key.replace("_", " ")}</span>
                  <strong>{Number(value).toFixed(4)}</strong>
                </div>
              ))
            ) : (
              <p className="empty-state">Train the model to populate evaluation metrics.</p>
            )}
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <h2>Predict Customer Risk</h2>
            <span>FastAPI inference endpoint</span>
          </div>
          <form className="prediction-form" onSubmit={handlePredict}>
            {Object.entries(form).map(([key, value]) => (
              <label key={key}>
                <span>{key.replaceAll("_", " ")}</span>
                <input name={key} value={value} onChange={updateField} />
              </label>
            ))}
            <button className="secondary-button" type="submit" disabled={loading}>
              Score Customer
            </button>
          </form>

          {prediction ? (
            <div className="prediction-result">
              <strong>Risk Score: {(prediction.churn_risk * 100).toFixed(1)}%</strong>
              <span>{prediction.predicted_label === 1 ? "Likely to churn" : "Likely to retain"}</span>
            </div>
          ) : null}
        </article>
      </section>
    </div>
  );
}
