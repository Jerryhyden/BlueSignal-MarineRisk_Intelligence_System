from datetime import datetime

zones = [

    # ✅ EASY / NORMAL (LOW)
    {
        "zone_id": 1,
        "zone_name": "Coral Bay",
        "latitude": 12.34,
        "longitude": 74.56,
        "baseline_ph": 8.1,
        "current_ph": 8.06,
        "temperature": 30,
        "salinity": 30,
        "dissolved_oxygen": 7,
        "timestamp": datetime.utcnow()
    },

    # ✅ EASY / NORMAL (LOW)
    {
        "zone_id": 5,
        "zone_name": "Blue Current",
        "latitude": 9.98,
        "longitude": 72.45,
        "baseline_ph": 8.1,
        "current_ph": 8.05,   # looks normal
        "temperature": 35,    # extreme heat
        "salinity": 42,       # abnormal salinity
        "dissolved_oxygen": 4.0,  # very low oxygen
        "timestamp": datetime.utcnow()
    },

    # ⚠ MODERATE STRESS
    {
        "zone_id": 3,
        "zone_name": "Delta Fisheries",
        "latitude": 11.78,
        "longitude": 73.89,
        "baseline_ph": 8.1,
        "current_ph": 5.70,   # moderate drop
        "temperature": 30,
        "salinity": 33,
        "dissolved_oxygen": 6.0,
        "timestamp": datetime.utcnow()
    },

    # 🔴 HIGH RISK
    {
        "zone_id": 4,
        "zone_name": "Eastern Shelf",
        "latitude": 10.55,
        "longitude": 76.12,
        "baseline_ph": 8.1,
        "current_ph": 7.40,   # severe drop
        "temperature": 32,
        "salinity": 31,
        "dissolved_oxygen": 5.0,
        "timestamp": datetime.utcnow()
    },

    # 🟣 ANOMALY (Normal pH but extreme environment)
    {
        "zone_id": 2,
        "zone_name": "Gulf Harvest",
        "latitude": 13.11,
        "longitude": 75.23,
        "baseline_ph": 8.1,
        "current_ph": 8.03,
        "temperature": 28,
        "salinity": 36,
        "dissolved_oxygen": 6.9,
        "timestamp": datetime.utcnow()
    }
]
