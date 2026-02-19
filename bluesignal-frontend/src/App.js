import React, { useEffect, useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { Bar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";
import "leaflet/dist/leaflet.css";
import "./App.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://localhost:8000/supply-chain")
      .then(response => {
        setZones(response.data?.zones || []);
        setLoading(false);
      })
      .catch(error => {
        console.error("API Error:", error);
        setLoading(false);
      });
  }, []);

  const getColor = (level) => {
    if (level === "LOW") return "#00e676";
    if (level === "MODERATE") return "#ffab00";
    return "#ff1744";
  };

  // =============================
  // HISTOGRAM DATA
  // =============================
  const barData = {
    labels: zones.map(z => z.zone_name),
    datasets: [{
      label: "Marine Stress Index",
      data: zones.map(z => z.stress_score || 0),
      backgroundColor: zones.map(z => getColor(z.stress_level)),
      borderRadius: 8
    }]
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#ffffff",
          font: {
            size: 14,
            weight: "bold",
            family: "Inter, sans-serif"
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: "#e0f7fa",
          font: {
            size: 14,
            weight: "600",
            family: "Inter, sans-serif"
          }
        },
        grid: {
          color: "rgba(255,255,255,0.05)"
        }
      },
      y: {
        ticks: {
          color: "#e0f7fa",
          font: {
            size: 14,
            weight: "600",
            family: "Inter, sans-serif"
          }
        },
        grid: {
          color: "rgba(255,255,255,0.05)"
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="container">
        <h1>🌊 BlueSignal Marine Intelligence</h1>
        <p>Loading marine intelligence data...</p>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>🌊 BlueSignal Marine Intelligence</h1>

      {/* ============================= */}
      {/* 1️⃣ ZONE TABLE */}
      {/* ============================= */}
      <h2>Zone Data Overview</h2>
      <table>
        <thead>
          <tr>
            <th>Zone</th>
            <th>pH</th>
            <th>Temp</th>
            <th>Salinity</th>
            <th>Oxygen</th>
            <th>Stress</th>
            <th>Risk Score</th>
          </tr>
        </thead>
        <tbody>
          {zones.map(zone => (
            <tr key={zone.zone_id}>
              <td>{zone.zone_name}</td>
              <td>{zone.current_ph ?? "--"}</td>
              <td>{zone.temperature ?? "--"}</td>
              <td>{zone.salinity ?? "--"}</td>
              <td>{zone.dissolved_oxygen ?? "--"}</td>
              <td style={{ color: getColor(zone.stress_level) }}>
                {zone.stress_level}
              </td>
              <td>
                <strong style={{
                  color:
                    zone.risk_score > 70 ? "#ff1744" :
                    zone.risk_score > 40 ? "#ffab00" :
                    "#00e676"
                }}>
                  {zone.risk_score ?? "--"}
                </strong>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* ============================= */}
      {/* 2️⃣ ZONE CARDS */}
      {/* ============================= */}
      <div className="card-grid">
        {zones.map(zone => {

          const trendData = {
            labels: ["T-3", "T-2", "T-1", "Now"],
            datasets: [{
              label: "Stress Trend",
              data: zone.stress_trend || [],
              borderColor: "#00e5ff",
              backgroundColor: "rgba(0,229,255,0.15)",
              tension: 0.4,
              fill: true
            }]
          };

          return (
            <div key={zone.zone_id} className="zone-card">

              <h3>{zone.zone_name}</h3>

              <div style={{
                fontSize: "28px",
                fontWeight: "bold",
                marginBottom: "10px",
                color:
                  zone.risk_score > 70 ? "#ff1744" :
                  zone.risk_score > 40 ? "#ffab00" :
                  "#00e676"
              }}>
                Risk Score: {zone.risk_score ?? "--"}
              </div>

              <p>Confidence: {zone.confidence_score ?? "--"}%</p>

              <div className="summary-box">
                <strong>Executive Insight:</strong>
                <p>{zone.executive_summary}</p>
              </div>

              <p style={{ fontWeight: "bold" }}>
                💰 Estimated Loss: ₹{zone.estimated_financial_loss?.toLocaleString() ?? 0}
              </p>

              <div className="env-box">
                <p>🌡 Temp: {zone.temperature ?? "--"}°C</p>
                <p>🌊 Salinity: {zone.salinity ?? "--"}</p>
                <p>🫧 Oxygen: {zone.dissolved_oxygen ?? "--"}</p>
              </div>

              <div className="ml-box">
                <p><strong>Predicted Stress:</strong> {zone.predicted_stress ?? "--"}</p>

                {zone.ai_warning && (
                  <p style={{ color: "#ff1744", fontWeight: "bold" }}>
                    ⚠ AI Forecast: High Risk Expected Soon
                  </p>
                )}

                {zone.anomaly_detected && (
                  <p style={{
                    color: "#39FF14",
                    fontWeight: "bold",
                    textShadow: "0 0 6px #39FF14"
                  }}>
                    🚨 Anomaly Detected
                  </p>
                )}
              </div>

              <div style={{ marginTop: "15px" }}>
                <Line data={trendData} />
              </div>

            </div>
          );
        })}
      </div>

      {/* ============================= */}
      {/* 3️⃣ HISTOGRAM */}
      {/* ============================= */}
      <div className="graph-row">
        <div className="graph-box">
          <h3>Marine Stress Histogram</h3>
          <Bar data={barData} options={barOptions} />
        </div>
      </div>

      {/* ============================= */}
      {/* 4️⃣ MAP */}
      {/* ============================= */}
      <div className="map-container">
        <MapContainer center={[12.97, 80.25]} zoom={5} style={{ height: "300px" }}>
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {zones.map(zone => (
            <CircleMarker
              key={zone.zone_id}
              center={[zone.latitude, zone.longitude]}
              radius={12}
          pathOptions={{
  color:
    zone.stress_level === "LOW" ? "#00e676" :
    zone.stress_level === "MODERATE" ? "#ffeb3b" :
    "#ff1744",
  fillColor:
    zone.stress_level === "LOW" ? "#00e676" :
    zone.stress_level === "MODERATE" ? "#ffeb3b" :
    "#ff1744",
  fillOpacity: 0.9,
  weight: 2
}}
            >
              <Popup>
                <strong>{zone.zone_name}</strong><br />
                Risk Score: {zone.risk_score}<br />
                Stress: {zone.stress_level}<br />
                Financial Loss: ₹{zone.estimated_financial_loss?.toLocaleString()}
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

    </div>
  );
}

export default App;
