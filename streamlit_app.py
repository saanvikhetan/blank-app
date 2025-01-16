
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# --- Data ---
# Define emission factors (replace with your actual values)
emission_factors = {
    "diet": {
        "Meat in every meal": 3.3,
        "Meat in some meals": 2.5,
        "Meat very rarely": 1.7,
        "Vegetarian": 1.2,
        "Vegan": 0.9,
    },
    "food_waste": {
        "None": 0,
        "0% - 10%": 0.1,
        "10% - 30%": 0.4,
        "More than 30%": 1.0,
    },
    "vehicle_use": {
        "Electric car": 1,
        "Hybrid car": 2,
        "Small petrol/diesel car": 3,
        "Medium petrol/diesel car": 4,
        "Large petrol/diesel car": 5,
        "Motorbike": 2.5,
        "Public Transport": 1.5,
        "Walking/Cycling": 0,
    },
    "home": {
        "Detached": 6,
        "Semi-detached": 4,
        "Terrace": 3,
        "Flat": 2,
    },
    "home_cooling": {  # Separate dictionary for cooling
        "I don’t use a cooler": 0,
        "Below 19°C": 3,
        "19°C - 23°C": 2,
        "24°C - 30°C": 1,
    },
    "home_improvements": -0.2,  # Reduction per improvement
    "stuff": {
        "TV, laptop, or PC": 0.2,
        "Large furniture": 0.3,
        "Washing machine, dishwasher, etc.": 0.4,
        "Mobile phone or tablet": 0.1,
        "Spending": {
            "₹0 - ₹5,000": 0.2,
            "₹5,000 - ₹15,000": 0.5,
            "₹15,000 - ₹30,000": 1,
            "Over ₹30,000": 1.5,
        },
    },
    "offsetting": {
        "Frequency": {
            "I never take offsetting actions": 0,
            "Rarely (once or twice a year)": -0.1,
            "Sometimes (a few times a year)": -0.3,
            "Often (monthly or more frequently)": -0.6,
            "Always (I actively offset regularly and for most of my activities)": -1,
        },
        "Actions": {
            "Donate to environmental projects": -0.2,
            "Participate in local initiatives": -0.3,
            "Purchase carbon credits": -0.2,
        },
    },
}

# --- Streamlit App ---
st.title("Carbon Footprint Calculator")

# --- DIET ---
st.header("Diet")
diet = st.selectbox(
    "How would you best describe your diet?",
    list(emission_factors["diet"].keys())
)
food_waste = st.selectbox(
    "Of the food you buy, how much is wasted and thrown away?",
    list(emission_factors["food_waste"].keys())
)

# --- TRAVEL ---
st.header("Travel")
vehicle = st.selectbox(
    "Which of these best describes the vehicle you use most?",
    list(emission_factors["vehicle_use"].keys())
)
hours_in_vehicle = st.slider(
    "How many hours a week do you spend in your car or on your motorbike for personal use?",
    0, 25, 5
)
public_transport_hours = st.slider(
    "How many hours a week do you spend on public transport (metro/train/bus) for personal use?",
    0, 25, 5
)
domestic_flights = st.number_input("Number of domestic flights in the last year:", min_value=0)
indian_subcontinent_flights = st.number_input(
    "Number of flights to the Indian Subcontinent in the last year:", min_value=0
)
international_flights = st.number_input(
    "Number of international flights in the last year:", min_value=0
)

# --- HOME ---
st.header("Home")
house_type = st.selectbox(
    "What kind of house do you live in?",
    list(emission_factors["home"].keys())
)
cooling = st.selectbox(
    "How cool is your house during summer?",
    list(emission_factors["home_cooling"].keys()),  # Use separate dictionary for cooling
)
home_improvements = st.multiselect(
    "Which of these home energy efficiency improvements are installed in your home?",
    [
        "Energy-saving lightbulbs",
        "Loft insulation",
        "Cavity or solid wall insulation",
        "Condensing boiler",
        "Double glazing",
        "Low flow fittings to taps and showers",
        "Solar panels",
        "Solar water heater",
    ],
)

# --- STUFF ---
st.header("Stuff")
new_items = st.multiselect(
    "In the last 12 months, have you bought any of these new household items?",
    [
        "TV, laptop, or PC",
        "Washing machine, dishwasher, etc.",
        "Mobile phone or tablet",
    ],
)
non_essential_spending = st.selectbox(
    "In a typical month, how much do you spend on non-essential items?",
    list(emission_factors["stuff"]["Spending"].keys()),
)

# --- OFFSETTING ---
st.header("Offsetting")
offsetting_frequency = st.selectbox(
    "How often do you take actions to offset your carbon footprint?",
    list(emission_factors["offsetting"]["Frequency"].keys()),
)
offsetting_actions = st.multiselect(
    "What types of offsetting actions do you take?",
    list(emission_factors["offsetting"]["Actions"].keys()),
)

# --- CALCULATIONS ---
def calculate_emissions():
    """Calculates the total annual carbon footprint."""
    # Diet
    diet_emissions = emission_factors["diet"][diet]

    # Food Waste
    food_waste_emissions = emission_factors["food_waste"][food_waste]

    # Travel
    vehicle_emissions = (
        emission_factors["vehicle_use"][vehicle] * hours_in_vehicle * 0.27
    )
    public_transport_emissions = (
        emission_factors["vehicle_use"]["Public Transport"] * public_transport_hours * 0.0833
    )
    flight_emissions = (
        domestic_flights * 0.5 + indian_subcontinent_flights * 1.5 + international_flights * 3
    )

    # Home
    home_emissions = emission_factors["home"][house_type]
    cooling_emissions = emission_factors["home_cooling"][cooling]  # Use separate dictionary
    home_improvements_emissions = emission_factors["home_improvements"] * len(home_improvements)

    # Stuff
    stuff_emissions = sum(
        emission_factors["stuff"].get(item, 0) for item in new_items
    ) + emission_factors["stuff"]["Spending"][non_essential_spending]

    # Offsetting
    offsetting_reductions = emission_factors["offsetting"]["Frequency"][offsetting_frequency]
    for action in offsetting_actions:
        offsetting_reductions += emission_factors["offsetting"]["Actions"].get(action, 0)

    # Category breakdown
    category_emissions = {
        "Diet": diet_emissions + food_waste_emissions,
        "Travel": vehicle_emissions + public_transport_emissions + flight_emissions,
        "Home": home_emissions + cooling_emissions + home_improvements_emissions,
        "Stuff": stuff_emissions,
    }

    # Total Emissions
    total_emissions = sum(category_emissions.values()) + offsetting_reductions

    return total_emissions, category_emissions

# --- Display Results ---
if st.button("Calculate"):
    total_emissions, category_emissions = calculate_emissions()

    st.success(f"Your estimated annual carbon footprint is: {total_emissions:.2f} tons of CO₂e")

    # Pie Chart
    st.header("Breakdown of Your Carbon Footprint")
    fig, ax = plt.subplots()
    labels = category_emissions.keys()
    sizes = category_emissions.values()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#FF9999", "#66B3FF", "#99FF99", "#FFCC99"])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Suggestions
    st.header("Personalized Suggestions")
    max_category = max(category_emissions, key=category_emissions.get)

    suggestions = {
        "Diet": "Consider reducing meat consumption or switching to a vegetarian or vegan diet to lower emissions from food production.",
        "Travel": "It seems as if your travel choices are influencing your carbon footprint the most. Here are a few steps you could take to cut down on travel emissions: use public transport if possible, take holidays closer to home, reduce flying, and walk if a destination is within walking distance.",
        "Home": "Improving your home energy efficiency can help. Consider installing energy-saving lightbulbs, loft insulation, double glazing, or solar panels to reduce energy consumption.",
        "Stuff": "Reducing the number of new items purchased or opting for second-hand goods can significantly cut emissions. Consider repairing items instead of replacing them and minimizing non-essential spending."
    }

    st.info(suggestions[max_category])

    # --- Additional Information ---
    st.markdown(
        """
        **Note:** This is a simplified estimation and may not reflect your actual carbon footprint accurately. 
        Consider consulting with a carbon footprint specialist for a more precise assessment.
        """
    )
    # --- Bar Graph ---
    st.header("Comparison to Global Averages")
    averages = {
        "Saudi Arabia": 22.1,
        "US": 14.3,
        "China": 8.4,
        "World": 4.7,
        "UK": 4.4,
        "India": 2.1,
        "You": total_emissions
    }
    averages_df = pd.DataFrame.from_dict(averages, orient='index', columns=['Carbon Footprint (tCO2e)'])

    fig, ax = plt.subplots()

    # Define a list of colors (ensure at least as many colors as countries)
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#edc948', '#8c564b', '#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    # Ensure enough colors
    num_bars = len(averages_df)
    if num_bars > len(colors):
        colors = colors * math.ceil(num_bars / len(colors)) 

    # Set the color for each bar using a loop
    for i, row in averages_df.iterrows():
        color_index = i % len(colors)  # Calculate the index correctly
        ax.bar(row.name, row['Carbon Footprint (tCO2e)'], color=colors[color_index])

    ax.set_ylabel("Carbon Footprint (tCO2e)")
    ax.set_title("Your Footprint vs. Global Averages")
    st.pyplot(fig)



