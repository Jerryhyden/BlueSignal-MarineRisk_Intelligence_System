# ---------------------------------------------------
# MULTI-FACTOR MARINE STRESS CALCULATION
# ---------------------------------------------------

def calculate_stress(zone):
    """
    Calculates marine stress using multiple environmental factors:
    - pH deviation
    - Temperature deviation
    - Salinity deviation
    - Dissolved oxygen deviation
    """

    # --- pH impact (primary driver)
    ph_impact = (zone["baseline_ph"] - zone["current_ph"]) * 100

    # --- Temperature impact (optimal ~27°C)
    temp_optimal = 27
    temp_impact = abs(zone.get("temperature", 27) - temp_optimal) * 5

    # --- Salinity impact (optimal ~35 PSU)
    salinity_optimal = 35
    salinity_impact = abs(zone.get("salinity", 35) - salinity_optimal) * 3

    # --- Dissolved Oxygen impact (optimal ~7 mg/L)
    oxygen_optimal = 7
    oxygen_impact = abs(zone.get("dissolved_oxygen", 7) - oxygen_optimal) * 8

    # --- Weighted combination
    stress_score = (
        0.4 * ph_impact +
        0.2 * temp_impact +
        0.2 * salinity_impact +
        0.2 * oxygen_impact
    )

    # --- Determine stress level
    if stress_score < 20:
        stress_level = "LOW"
    elif stress_score < 50:
        stress_level = "MODERATE"
    else:
        stress_level = "HIGH"

    return round(stress_score, 2), stress_level


# ---------------------------------------------------
# SUPPLY CHAIN DECISION ENGINE
# ---------------------------------------------------

def supply_chain_decision(stress_level):

    if stress_level == "HIGH":
        return {
            "certification_status": "Suspended",
            "freight_route": "Reroute to Alternative Zone",
            "consumer_label": "Under Ecological Review"
        }

    elif stress_level == "MODERATE":
        return {
            "certification_status": "Conditional",
            "freight_route": "Monitor Closely",
            "consumer_label": "Caution"
        }

    else:
        return {
            "certification_status": "Active",
            "freight_route": "Normal",
            "consumer_label": "Stable"
        }
