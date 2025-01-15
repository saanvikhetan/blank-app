import streamlit as st

def calculate_carbon_footprint(answers):
    """Calculates carbon footprint based on user answers."""

    emissions = 0

    # Diet
    diet_emissions = {
        "Meat in every meal": 3.3,
        "Meat in some meals": 2.5,
        "Meat very rarely": 1.7,
        "Vegetarian": 1.2,
        "Vegan": 0.9,
    }
    emissions += diet_emissions.get(answers["diet"], 0)

    # Food Waste
    waste_emissions = {
        "None": 0,
        "0% - 10%": 0.1,
        "10% - 30%": 0.4,
        "More than 30%": 1.0,
    }
    emissions += waste_emissions.get(answers["food_waste"], 0)

    # Travel (simplified, needs more detailed calculation for hours and flights)
    vehicle_emissions = {
        "Electric car": 1,
        "Hybrid car": 2,
        "Small petrol/diesel car": 3,
        "Medium petrol/diesel car": 4,
        "Large petrol/diesel car": 5,
        "Public Transport": 1.5,
        "Neither - I walk or cycle for most of my journeys": 0,
    }
    emissions += vehicle_emissions.get(answers["vehicle"], 0)

    # Home
    home_emissions = {
        "Detached": 6,
        "Semi-detached": 4,
        "Terrace": 3,
        "Flat": 2,
    }
    emissions += home_emissions.get(answers["house_type"], 0)

    cooling_emissions = {
      "I don’t use a cooler": 0,
      "Below 19°C (very cold)": 3,
      "19°C - 23°C (moderately cool)": 2,
      "24°C - 30°C (energy-saving)": 1
    }
    emissions += cooling_emissions.get(answers["house_cool"],0)

    # Stuff (simplified)
    stuff_emissions = 0
    if answers.get("tv_laptop", False): stuff_emissions += 0.2
    if answers.get("furniture", False): stuff_emissions += 0.3
    if answers.get("appliance", False): stuff_emissions += 0.4
    if answers.get("phone", False): stuff_emissions += 0.1
    emissions += stuff_emissions

    # Offsetting (Simplified)
    offset_reductions = {
        "I never take offsetting actions": 0,
        "Rarely (once or twice a year)": 0.1,
        "Sometimes (a few times a year)": 0.3,
        "Often (monthly or more frequently)": 0.6,
        "Always (I actively offset regularly and for most of my activities)": 1,
    }
    emissions -= offset_reductions.get(answers["offset_frequency"],0)

    return emissions

st.title("Carbon Footprint Calculator")

answers = {}

# Diet
answers["diet"] = st.selectbox("How would you best describe your diet?",
    ["Meat in every meal", "Meat in some meals", "Meat very rarely", "Vegetarian", "Vegan"])

answers["food_waste"] = st.selectbox("Of the food you buy, how much is wasted?",
    ["None", "0% - 10%", "10% - 30%", "More than 30%"])

# Travel
answers["vehicle"] = st.selectbox("Which vehicle do you use most?",
    ["Electric car", "Hybrid car", "Small petrol/diesel car", "Medium petrol/diesel car", "Large petrol/diesel car", "Public Transport", "Neither - I walk or cycle for most of my journeys"])

# Home
answers["house_type"] = st.selectbox("What kind of house do you live in?", ["Detached", "Semi-detached", "Terrace", "Flat"])
answers["house_cool"] = st.selectbox("How cool is your house during summer?", ["I don’t use a cooler","Below 19°C (very cold)", "19°C - 23°C (moderately cool)", "24°C - 30°C (energy-saving)"])

# Stuff
st.subheader("Stuff")
answers["tv_laptop"] = st.checkbox("Bought a TV, laptop, or PC in the last 12 months")
answers["furniture"] = st.checkbox("Bought a large item of furniture in the last 12 months")
answers["appliance"] = st.checkbox("Bought a washing machine, dishwasher, etc. in the last 12 months")
answers["phone"] = st.checkbox("Bought a mobile phone or tablet in the last 12 months")

# Offsetting
answers["offset_frequency"] = st.selectbox("How often do you take actions to offset your carbon footprint?",
    ["I never take offsetting actions", "Rarely (once or twice a year)", "Sometimes (a few times a year)", "Often (monthly or more frequently)", "Always (I actively offset regularly and for most of my activities)"])


if st.button("Calculate"):
    footprint = calculate_carbon_footprint(answers)
    st.write(f"Your estimated annual carbon footprint is: {footprint:.2f} tons of CO₂e")




