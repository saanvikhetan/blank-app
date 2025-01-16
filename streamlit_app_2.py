import streamlit as st import pandas as pd import matplotlib.pyplot as plt import seaborn as sns # --- (Your original code for data and user input) --- def calculate_emissions(): """Calculates the total annual carbon footprint.""" # --- Data --- 
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
"Cooling": { 
"I don’t use a cooler": 0, 
"Below 19°C": 3, 
"19°C - 23°C": 2, 
"24°C - 30°C": 1, 
}, 
"Improvements": -0.2, # Reduction per improvement 
}, 
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
"What kind of house do you live in?", list(emission_factors["home"].keys()) 
) 
cooling = st.selectbox( 
"How cool is your house during summer?", 
list(emission_factors["home"]["Cooling"].keys()), 
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
"Large item of furniture", 
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
emission_factors["vehicle_use"][vehicle] 
* hours_in_vehicle 
) 
public_transport_emissions = ( 
emission_factors["vehicle_use"]["Public Transport"] 
* public_transport_hours 
) 
flight_emissions = ( 
domestic_flights * 0.5 
+ indian_subcontinent_flights * 1.5 
+ international_flights * 3 
) 
# Home 
home_emissions = emission_factors["home"][house_type] 
home_emissions += emission_factors["home"]["Cooling"][cooling] 
home_emissions += emission_factors["home"]["Improvements"] * len(home_improvements) 
# Stuff 
stuff_emissions = sum( 
emission_factors["stuff"][item] for item in new_items 
) + emission_factors["stuff"]["Spending"][non_essential_spending] 
# Offsetting 
offsetting_reductions = emission_factors["offsetting"]["Frequency"][offsetting_frequency] 
for action in offsetting_actions: 
offsetting_reductions += emission_factors["offsetting"]["Actions"][action] 
# Total Emissions 
total_emissions = ( 
diet_emissions 
+ food_waste_emissions 
+ vehicle_emissions 
+ public_transport_emissions 
+ flight_emissions 
+ home_emissions 
+ stuff_emissions 
+ offsetting_reductions 
) 
return total_emissions 
# --- Display Results --- 
if st.button("Calculate"): 
total_emissions = calculate_emissions() 
st.success(f"Your estimated annual carbon footprint is: {total_emissions:.2f} tons of CO₂e") 
# --- Additional Information --- 
st.markdown( 
""" 
**Note:** This is a simplified estimation and may not reflect your actual carbon footprint accurately. 
Consider consulting with a carbon footprint specialist for a more precise assessment. 
""" 
)
 Calculate emissions for each category emissions_by_category = { "Diet": diet_emissions,"Food Waste": food_waste_emissions, "Travel": vehicle_emissions + public_transport_emissions + flight_emissions,"Home": home_emissions, "Stuff": stuff_emissions, } return total_emissions, emissions_by_category # --- Display Results --- if st.button("Calculate"): total_emissions, emissions_by_category = calculate_emissions() st.success(f"Your estimated annual carbon footprint is: {total_emissions:.2f} tons of CO₂e") # Create a pie chart fig, ax = plt.subplots() plt.pie(emissions_by_category.values(), labels=emissions_by_category.keys(), autopct='%1.1f%%') plt.title("Carbon Footprint Breakdown") plt.legend() st.pyplot(fig) st.header("Personalized Recommendations") for category, emissions inemissions_by_category.items(): if emissions > 0.5 * total_emissions:  # If a category contributes more than 50%st.write(f"**{category}:**") if category == "Travel": st.write("- **Weekly Goal:**") st.write(" - Use public transport at least twice this week instead of driving.") st.write(" - Carpool or bike to work/school once this week.") st.write(" - Plan a car-free day for errands.") st.write("- **Daily Goal:**") st.write(" - Walk or bike for short trips instead of driving.") st.write(" - Consider telecommuting one day per week.") elif category == "Home": st.write("- **Weekly Goal:**") st.write(" - Unplug electronics from the wall when not in use one day this week.") st.write(" - Do a short energy audit of your home (check for drafts, etc.).") st.write(" - Wash clothes in cold water.") st.write("- **Daily Goal:**") st.write(" - Turn off lights and appliances when leaving a room.") st.write(" - Take shorter showers.") elif category == "Diet": st.write("- **Weekly Goal:**") st.write(" - Cook a meat-free meal at least twice this week.") st.write(" - Plan and shop for meals to reduce food waste.") st.write(" - Visit a local farmers' market.") st.write("- **Daily Goal:**") st.write(" - Store food properly to prevent spoilage.") st.write(" - Eat smaller portions.") elif category == "Stuff": st.write("- **Weekly Goal:**") st.write(" - Repair one broken item instead of throwing it away.") st.write(" - Borrow, rent, or buy used items whenever possible.") st.write(" - Declutter and donate unwanted items.") st.write("- **Daily Goal:**") st.write(" - Think twice before making any non-essential purchases.") st.write(" - Choose products with minimal packaging.")
