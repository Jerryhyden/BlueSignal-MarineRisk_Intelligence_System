from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import zones
from services import calculate_stress, supply_chain_decision
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ML imports
from ml_model import predict_future_stress, detect_anomaly

app = FastAPI(title="BlueSignal - Marine Risk Intelligence")

# ---------------------------------------------------
# CORS
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# EMAIL CONFIG
# ---------------------------------------------------
SENDER_EMAIL = "askarnasar3@gmail.com"
SENDER_PASSWORD = "tkqujvpddjtftpjk"
RECEIVER_EMAIL = "jerryhyden2005@gmail.com"

# ---------------------------------------------------
# EMAIL FUNCTION
# ---------------------------------------------------
def send_email_alert(zone_name, alert_message, yield_drop, insurance_risk):

    subject = f"🚨 Marine Alert: {zone_name}"

    body = f"""
High Marine Risk Detected!

Zone: {zone_name}
Message: {alert_message}
Estimated Yield Drop: {yield_drop}%
Insurance Risk Level: {insurance_risk}

Triggered At: {datetime.utcnow()}

- BlueSignal System
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email sending failed:", e)

# ---------------------------------------------------
# ECONOMIC ALERT ENGINE
# ---------------------------------------------------
def economic_alert_engine(stress_score: float):

    if stress_score < 20:
        return {
            "alert_level": "LOW",
            "message": "Ocean Stable – Normal Fish Yield Expected",
            "yield_drop_percent": 0,
            "insurance_risk": "Low"
        }

    elif stress_score < 50:
        return {
            "alert_level": "MODERATE",
            "message": "Moderate Marine Stress – Yield Reduction Possible",
            "yield_drop_percent": 10,
            "insurance_risk": "Moderate"
        }

    else:
        return {
            "alert_level": "HIGH",
            "message": "Severe Marine Stress – High Economic Risk",
            "yield_drop_percent": 20,
            "insurance_risk": "Elevated"
        }

# ---------------------------------------------------
# EXECUTIVE SUMMARY GENERATOR
# ---------------------------------------------------
def generate_executive_summary(zone_name, risk_score, anomaly_flag):

    if anomaly_flag:
        return f"{zone_name} is showing unusual environmental behavior. Immediate monitoring recommended."

    if risk_score > 70:
        return f"{zone_name} is in high economic risk territory. Yield impact expected."

    if risk_score > 40:
        return f"{zone_name} shows moderate stress trends that may affect operations."

    return f"{zone_name} is currently stable with low marine risk."

# ---------------------------------------------------
# GET ALL ZONES
# ---------------------------------------------------
@app.get("/zones")
def get_zones():
    return zones

# ---------------------------------------------------
# GET SUPPLY CHAIN WITH STABLE INTELLIGENCE
# ---------------------------------------------------
@app.get("/supply-chain")
def get_supply_chain():

    results = []
    global_alert_flag = False
    BASELINE_REVENUE = 10000000  # ₹1 Crore demo baseline

    for zone in zones:

        # -------------------------
        # Stress Calculation
        # -------------------------
        stress_score, stress_level = calculate_stress(zone)

        # -------------------------
        # Safe ML Prediction
        # -------------------------
        predicted_stress = predict_future_stress(zone)

        # Clamp prediction
        predicted_stress = max(0, min(predicted_stress, 120))

        # -------------------------
        # Anomaly Detection
        # -------------------------
        anomaly_flag = detect_anomaly(zone)

        decision = supply_chain_decision(stress_level)
        alert = economic_alert_engine(stress_score)

        # -------------------------
        # Email Trigger
        # -------------------------
        # if zone.get("current_ph", 8.1) <= 7.7:
        #     global_alert_flag = True
        if zone.get("current_ph", 8.1) <= 7.7:
            global_alert_flag = True
            send_email_alert(
                zone["zone_name"],
                alert["message"],
                alert["yield_drop_percent"],
                alert["insurance_risk"]
    )

        # -------------------------
        # AI Warning
        # -------------------------
        ai_warning = predicted_stress >= 50

        # -------------------------
        # Composite Risk Score (Balanced)
        # -------------------------
        anomaly_weight = 15 if anomaly_flag else 0

        risk_score = (
            (0.6 * stress_score) +
            (0.3 * predicted_stress) +
            anomaly_weight
        )

        risk_score = round(min(max(risk_score, 0), 100), 2)

        # -------------------------
        # Financial Impact
        # -------------------------
        estimated_loss = round(
            BASELINE_REVENUE * (alert["yield_drop_percent"] / 100),
            2
        )

        # -------------------------
        # Stress Trend (Stable Simulation)
        # -------------------------
        stress_trend = [
            round(max(stress_score - 15, 0), 2),
            round(max(stress_score - 8, 0), 2),
            round(max(stress_score - 3, 0), 2),
            round(stress_score, 2)
        ]

        # -------------------------
        # Confidence Score (Stable)
        # -------------------------
        confidence_score = 100 - abs(predicted_stress - stress_score)
        confidence_score = round(min(max(confidence_score, 50), 100), 2)

        # -------------------------
        # Executive Summary
        # -------------------------
        executive_summary = generate_executive_summary(
            zone["zone_name"],
            risk_score,
            anomaly_flag
        )

        # -------------------------
        # Append Result
        # -------------------------
        results.append({
            "zone_id": zone["zone_id"],
            "zone_name": zone["zone_name"],
            "latitude": zone["latitude"],
            "longitude": zone["longitude"],

            "baseline_ph": zone.get("baseline_ph"),
            "current_ph": zone.get("current_ph"),
            "temperature": zone.get("temperature"),
            "salinity": zone.get("salinity"),
            "dissolved_oxygen": zone.get("dissolved_oxygen"),
            "timestamp": zone.get("timestamp"),

            "stress_score": stress_score,
            "stress_level": stress_level,
            "predicted_stress": predicted_stress,
            "risk_score": risk_score,
            "confidence_score": confidence_score,
            "stress_trend": stress_trend,
            "ai_warning": ai_warning,
            "anomaly_detected": anomaly_flag,

            "estimated_financial_loss": estimated_loss,

            "certification_status": decision["certification_status"],
            "freight_route": decision["freight_route"],
            "consumer_label": decision["consumer_label"],
            "economic_alert": alert,
            "executive_summary": executive_summary
        })

    return {
        "global_alert": global_alert_flag,
        "zones": results
    }

# ---------------------------------------------------
# SIMULATE pH DROP
# ---------------------------------------------------
@app.post("/simulate-drop")
def simulate_drop(zone_id: int, drop_value: float):

    for zone in zones:
        if zone["zone_id"] == zone_id:

            zone["current_ph"] -= drop_value
            zone["timestamp"] = datetime.utcnow()

            return {"message": "pH updated successfully"}

    raise HTTPException(status_code=404, detail="Zone not found")
@app.get("/")
def root():
    return {"message": "BlueSignal Marine Intelligence API Running"}
