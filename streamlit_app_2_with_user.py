import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import users as user_lib


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
}

# Suggestions categorized by Diet, Travel, Home, and Stuff
suggestions_data = {
    "Diet": [
        {"action": "Switch to a vegetarian diet", "points": 50},
        {"action": "Have one meat-free day per week", "points": 20},
        {"action": "Reduce food waste by 10%", "points": 30},
        {"action": "Eat a plant-based diet", "points": 60},
        {"action": "Choose local and seasonal produce", "points": 40},
        {"action": "Avoid food waste", "points": 50},
        {"action": "Reduce consumption of processed foods", "points": 30},
        {"action": "Support sustainable farming practices", "points": 45},
    ],
    "Travel": [
        {"action": "Use public transport for a week", "points": 40},
        {"action": "Walk or cycle instead of driving for short trips", "points": 30},
        {"action": "Avoid one domestic flight", "points": 70},
        {"action": "Use public transportation or carpool", "points": 50},
        {"action": "Bike or walk for short distances", "points": 35},
        {"action": "Reduce air travel", "points": 100},
        {"action": "Drive an electric or hybrid vehicle", "points": 80},
        {"action": "Combine trips to reduce car use", "points": 25},
    ],
    "Home": [
        {"action": "Install energy-efficient lightbulbs", "points": 25},
        {"action": "Use a fan instead of air conditioning", "points": 30},
        {"action": "Install solar panels", "points": 100},
        {"action": "Install energy-efficient appliances", "points": 60},
        {"action": "Use LED lighting", "points": 20},
        {"action": "Insulate your home", "points": 75},
        {"action": "Switch to renewable energy", "points": 90},
        {"action": "Lower thermostat settings in winter and raise them in summer", "points": 40},
    ],
    "Stuff": [
        {"action": "Buy second-hand items", "points": 30},
        {"action": "Repair instead of replacing an item", "points": 40},
        {"action": "Reduce monthly non-essential spending by 10%", "points": 50},
        {"action": "Reduce, reuse, recycle", "points": 70},
        {"action": "Buy second-hand or refurbished items", "points": 40},
        {"action": "Avoid single-use plastics", "points": 60},
        {"action": "Repair instead of replacing", "points": 50},
        {"action": "Support sustainable brands", "points": 45},
    ],
}

# Progress levels and badges
progress_levels = [
    {"title": "Eco Newbie", "points": [0, 500], "description": "Welcome to the world of sustainability! You're just starting your eco-friendly journey and taking your first steps toward reducing your carbon footprint. Engage in basic actions like meat-free days, buying second-hand items, or using public transport."},
    {"title": "Green Enthusiast", "points": [501, 1000], "description": "You're becoming more eco-conscious! Your commitment to reducing your footprint is growing, and you're making significant strides in your sustainability efforts. Start making eco-friendly choices regularly, such as reducing food waste and choosing sustainable farming practices."},
    {"title": "Sustainability Advocate", "points": [1001, 2000], "description": "You're actively promoting sustainable living. Your eco-conscious habits are becoming a regular part of your lifestyle, and you're encouraging others to make a change. Regularly use energy-efficient appliances, reduce processed foods, and make conscious decisions about waste and consumption."},
    {"title": "Planet Saver", "points": [2001, 3500], "description": "You're making a noticeable impact on the planet! Your dedication to sustainability is clear in both your actions and your lifestyle choices. Keep up the great work! Make major changes, such as installing solar panels, reducing air travel, and embracing renewable energy."},
    {"title": "Eco Warrior", "points": [3501, 5000], "description": "You’ve become a true warrior for the environment! Your commitment to sustainability is helping to lead the way for others, and your daily choices are making a real difference. Drive an electric vehicle, support sustainable brands, and implement energy-efficient systems in your home."},
    {"title": "Zero-Carbon Champion", "points": [5001, 7000], "description": "You’ve achieved a highly sustainable lifestyle! You've reduced your carbon footprint to a remarkable level and continue to advocate for climate action. Your lifestyle is fully aligned with eco-conscious choices, such as living zero waste, eliminating single-use plastics, and significantly reducing your carbon emissions."},
    {"title": "Planet Protector", "points": [7001, 8690], "description": "You are a true protector of the planet! Your relentless pursuit of sustainability has reduced your environmental impact to its minimum, and you're leading the charge for a greener future. Your efforts to reduce CO2 emissions through sustainable travel, energy, food, and lifestyle choices are exemplary. You’ve embraced every aspect of eco-friendly living."}
]

# Function to determine user's progress level and badge
def get_progress_level(points):
    for level in progress_levels:
        if level["points"][0] <= points <= level["points"][1]:
            return level
    return None

# --- Streamlit App ---
st.title("Carbon Footprint Calculator")

# Initialize session state for goals and points
if "goals" not in st.session_state:
    st.session_state.goals = []
if "eco_points" not in st.session_state:
    st.session_state.eco_points = 0


if "logged_in_userid" not in st.session_state:
    user_lib.show_users_login()
    menu = None
else:
    menu = st.radio("Navigation", ["Home", "Suggestions", "Goals", "Offset"])

# Sidebar for displaying points and level
if user_lib.is_user_logged_in() and "eco_points" in st.session_state:
    progress_level = get_progress_level(st.session_state.eco_points)
    if progress_level:
        st.sidebar.header(user_lib.get_logged_in_user_name() + ", Your Progress")
        st.sidebar.write(f"**{progress_level['title']}**")
        st.sidebar.write(progress_level["description"])
        st.sidebar.write(f"Points: {st.session_state.eco_points}")
        user_lib.show_logout_button(sidebar=True)
        st.sidebar.write(st.session_state)


# --- Home Section ---
if user_lib.is_user_logged_in() and menu == "Home":
    st.header("Calculate Your Carbon Footprint")

    # --- DIET ---
    st.subheader("Diet")
    diet = st.selectbox(
        "How would you best describe your diet?",
        list(emission_factors["diet"].keys())
    )
    food_waste = st.selectbox(
        "Of the food you buy, how much is wasted and thrown away?",
        list(emission_factors["food_waste"].keys())
    )

    # --- TRAVEL ---
    st.subheader("Travel")
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
    st.subheader("Home")
    house_type = st.selectbox(
        "What kind of house do you live in?",
        list(emission_factors["home"].keys())
    )
    cooling = st.selectbox(
        "How cool is your house during summer?",
        list(emission_factors["home_cooling"].keys()),  # Use separate dictionary for cooling
    )
    

    # --- STUFF ---
    st.subheader("Stuff")
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
        

        # Stuff
        stuff_emissions = sum(
            emission_factors["stuff"].get(item, 0) for item in new_items
        ) + emission_factors["stuff"]["Spending"][non_essential_spending]

        

        # Category breakdown
        category_emissions = {
            "Diet": diet_emissions + food_waste_emissions,
            "Travel": vehicle_emissions + public_transport_emissions + flight_emissions,
            "Home": home_emissions + cooling_emissions,
            "Stuff": stuff_emissions,
        }

        # Total Emissions
        total_emissions = sum(category_emissions.values())

        return total_emissions, category_emissions

    # --- Display Results ---
    if st.button("Calculate"):
        total_emissions, category_emissions = calculate_emissions()
        st.session_state.total_emissions = total_emissions
        st.session_state.category_emissions = category_emissions
        st.session_state.max_category = max(category_emissions, key=category_emissions.get)

        st.success(f"Your estimated annual carbon footprint is: {total_emissions:.2f} tons of CO₂e")

        # Pie Chart
        st.header("Breakdown of Your Carbon Footprint")
        fig, ax = plt.subplots()
        labels = category_emissions.keys()
        sizes = category_emissions.values()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#FF9999", "#66B3FF", "#99FF99", "#FFCC99"])
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

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

        # Define a dictionary to map countries to colors
        colors = {
            "Saudi Arabia": "#dc143c",
            "US": "#4169e1",
            "China": "#3cb371",
            "World": "#000080",
            "UK": "#40e0d0",
            "India": "#ff7f50",
            "You": "#8b008b"
        }

        # Plot the bars with assigned colors
        for country, value in averages.items():
            ax.bar(country, value, color=colors[country])

        ax.set_ylabel("Carbon Footprint (tCO2e)")
        ax.set_title("Your Footprint vs. Global Averages")
        st.pyplot(fig)

        # --- Personalized Goals ---
        st.header("Personalized Goals")

        weekly_goals = {
            "Diet": "Reduce meat consumption to 2-3 times a week.",
            "Travel": "Use public transport or walk/bike for at least 3 days a week.",
            "Home": "Implement one energy-saving home improvement per month.",
            "Stuff": "Limit non-essential purchases to once a week."
        }

        daily_goals = {
            "Diet": "Incorporate at least one vegetarian meal per day.",
            "Travel": "Use public transport or walk/bike for short distances daily.",
            "Home": "Turn off lights and appliances when not in use.",
            "Stuff": "Avoid buying non-essential items on a daily basis."
        }

        max_category = st.session_state.max_category

        st.subheader(f"Weekly Goal for {max_category}")
        st.write(weekly_goals[max_category])

        st.subheader(f"Daily Goal for {max_category}")
        st.write(daily_goals[max_category])

# --- Suggestions Section ---
if user_lib.is_user_logged_in() and menu == "Suggestions":
    st.header("Eco-Friendly Actions and Suggestions")
    for category, actions in suggestions_data.items():
        st.subheader(category)
        for suggestion in actions:
            st.write(f"- {suggestion['action']} (+{suggestion['points']} points)")

# --- Goals Section ---

goals_data = {
    "Food": [
        {"action": "Have one meat-free day per week", "carbon_reduction": 0.078, "points": 50},
        {"action": "Eat a plant-based diet", "carbon_reduction": 0.80, "points": 500},
        {"action": "Choose local and seasonal produce for 75% of meals", "carbon_reduction": 0.137, "points": 75},
        {"action": "Avoid food waste by 25%", "carbon_reduction": 0.012, "points": 40},
        {"action": "Reduce consumption of processed foods by 25%", "carbon_reduction": 0.05, "points": 25},
        {"action": "Support sustainable farming practices (e.g., certified organic)", "carbon_reduction": 1, "points": 200}
    ],
    "Travel": [
        {"action": "Walk or cycle instead of driving for 5 short trips per week", "carbon_reduction": 0.028, "points": 25},
        {"action": "Use public transportation or carpool for 3 trips per week", "carbon_reduction": 0.1, "points": 50},
        {"action": "Bike or walk for 3 short distances per week", "carbon_reduction": 0.03, "points": 25},
        {"action": "Take no more than 2 domestic flights per year", "carbon_reduction": 1, "points": 500},
        {"action": "Drive an electric or hybrid vehicle instead of normal", "carbon_reduction": 1, "points": 800},
        {"action": "Combine 2 trips per week to reduce car use", "carbon_reduction": 0.05, "points": 25}
    ],
    "Home": [
        {"action": "Install energy-efficient lightbulbs in all fixtures", "carbon_reduction": 0.03, "points": 50},
        {"action": "Use a fan instead of air conditioning for 3 months", "carbon_reduction": 0.04, "points": 50},
        {"action": "Replace 1 major appliance with an energy-efficient model", "carbon_reduction": 0.125, "points": 50},
        {"action": "Use LED lighting in all fixtures", "carbon_reduction": 0.05, "points": 75},
        {"action": "Insulate your loft", "carbon_reduction": 0.5, "points": 200},
        {"action": "Switch to a 100% renewable energy supplier", "carbon_reduction": 2, "points": 1500},
        {"action": "Lower thermostat by 1°C in winter and raise by 1°C in summer", "carbon_reduction": 0.1, "points": 50},
        {"action": "Cavity or solid wall insulation (if applicable)", "carbon_reduction": 1, "points": 500},
        {"action": "Condensing boiler (if replacing an old boiler)", "carbon_reduction": 1.2, "points": 600},
        {"action": "Double glazing all windows (if not already done)", "carbon_reduction": 0.8, "points": 400},
        {"action": "Low flow fittings to all taps and showers", "carbon_reduction": 0.2, "points": 100},
        {"action": "Solar water heater (if suitable for your location)", "carbon_reduction": 0.8, "points": 400}
    ],
    "Stuff": [
        {"action": "Buy at least 5 second-hand instead of new items per year", "carbon_reduction": 0.2, "points": 200},
        {"action": "Repair 2 items instead of replacing them", "carbon_reduction": 0.1, "points": 150},
        {"action": "Reduce monthly non-essential spending by 5%", "carbon_reduction": 0.05, "points": 100},
        {"action": "Reduce, reuse, recycle consistently (e.g., weekly)", "carbon_reduction": 0.5, "points": 250},
        {"action": "Buy second-hand or refurbished electronics", "carbon_reduction": 0.15, "points": 200},
        {"action": "Avoid single-use plastics for 3 meals per week", "carbon_reduction": 0.03, "points": 100},
        {"action": "Repair 1 major household item instead of replacing it", "carbon_reduction": 0.1, "points": 200},
        {"action": "Support 2 sustainable brands per year", "carbon_reduction": 0.25, "points": 400}
    ],
    "Other": [
        {"action": "Donate $50 to a reputable environmental organization", "carbon_reduction": 0.2, "points": 200},
        {"action": "Participate in 2 local environmental initiatives per year", "carbon_reduction": 0.3, "points": 400},
        {"action": "Purchase $50 of carbon offsets", "carbon_reduction": 0.2, "points": 200}
    ]
}
import streamlit as st

# Initialize session state variables if not already present
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'completed_goals' not in st.session_state:
    st.session_state.completed_goals = []


import streamlit as st

# Initialize session state variables if not already present
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'completed_goals' not in st.session_state:
    st.session_state.completed_goals = []

if user_lib.is_user_logged_in() and menu == "Goals":
    st.header("Set and Track Your Goals")

    # Flatten goals data into a list of actions with categories, carbon reduction, and points
    available_actions = [
        {
            "action": action["action"],
            "points": action["points"],
            "category": category,
            "carbon_reduction": action["carbon_reduction"]
        }
        for category, actions in goals_data.items()
        for action in actions
    ]

     # Filter out actions that are already in the user's goals or completed goals
    added_actions = [goal["action"] for goal in st.session_state.goals + st.session_state.completed_goals]
    available_actions = [
        action for action in available_actions
        if action["action"] not in added_actions
    ]
        
    # Category options for goal selection
    selected_category = st.selectbox("Choose a category:", list(goals_data.keys()))
    category_actions = [a for a in available_actions if a["category"] == selected_category]
    selected_action = st.selectbox("Choose an action to add to your goals:", [a["action"] for a in category_actions])

    if st.button("Add to Goals"):
        action_to_add = next((a for a in category_actions if a["action"] == selected_action), None)
        if action_to_add and action_to_add not in st.session_state.goals:
            st.session_state.goals.append(action_to_add)
            st.success(f"Added '{selected_action}' to your goals!")
        elif action_to_add:
            st.warning(f"'{selected_action}' is already in your goals.")

    # Display current goals with "Mark as Completed" buttons
    if st.session_state.goals:
        st.subheader("Your Goals")
        updated_goals = []
        for i, goal in enumerate(st.session_state.goals):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"- {goal['action']} ({goal['category']}, +{goal['points']} points)")
            with col2:
                if st.button(f"Mark as Completed ({goal['points']})", key=f"complete_{i}"):
                    if goal not in st.session_state.completed_goals:
                        st.session_state.completed_goals.append(goal)
                else:
                    updated_goals.append(goal)
        st.session_state.goals = updated_goals

   # Display completed goals
if st.session_state.completed_goals:
    st.subheader("Completed Goals")
    st.markdown("<p style='color:green;'>", unsafe_allow_html=True)
    for goal in st.session_state.completed_goals:
        st.write(f"- {goal['action']} ({goal['category']}, +{goal['points']} points)")
    st.markdown("</p>", unsafe_allow_html=True)
    st.write(f"Total Eco Points: {sum(goal['points'] for goal in st.session_state.completed_goals)}")

# Calculate and display total eco points (for all goals)
total_points = sum(goal['points'] for goal in st.session_state.goals) + sum(goal['points'] for goal in st.session_state.completed_goals)
st.write(f"Total Eco Points (All Goals): {total_points}")

# Update session state with total points
st.session_state.eco_points = total_points
# --- Offset Section ---
if user_lib.is_user_logged_in() and menu == "Offset":
    st.header("Offset Your Carbon Footprint")
    
    offset_links = {
        "HelpUsGreen": {
            "url": "https://www.helpusgreen.com/",
            "description": "By upcycling discarded temple flowers, they craft luxurious, eco-friendly incense. Therefore, fostering community growth and environmental conservation."
        },
        "Grow Trees": {
            "url": "https://www.grow-trees.com/index.php",
            "description": "With 20 million trees planted over almost 150 projects, Grow Trees is an environmental organization dedicated to facilitating tree planting through online platforms. They`ve recently started a project called Ratan Tata memorial forest, which will have a positive impact on carbon reduction, restoring forests and improving wildlife habitats."
        },
        "Solar Aid": {
            "url": "https://solar-aid.org/",
            "description": "Igniting kerosene lamps and paraffin candles can emit toxic fumes into people’s lungs and into the earth’s atmosphere, and in small towns this is the only option when the sun goes down. However, due to the use of solar power light, a real sustainable change can happen."
        },
        "TNC India": {
            "url": "https://www.tncindia.in/what-we-do/our-priorities/support-renewable-energy/",
            "description": "Their aim is to increase the use of readily available, cost-effective climate solutions such as reforestation, and implement policy changes to increase the rate of their transition to a clean energy future."
        },
        "WWF India": {
            "url": "https://join.wwfindia.org/?source=WWF-JOIN-WEB&utm_source=main_website&utm_medium=nav_link&utm_campaign=donate",
            "description": "WWF is an environmental organization whose main aims are to to improve environmental literacy, spread awareness on how to lower carbon footprint, preserve India’s vast wildlife heritage and to empower vulnerable groups through policy changes and on ground initiatives."
        },
        "BJSM": {
            "url": "https://bjsm.org.in/donations/donate-to-protect-the-environment/",
            "description": "This is one of India’s top NGO where they are dedicated to starting initiatives that combat climate change, focus on sustainable land management, aim to ensure clean and sufficient water resources and to promote agroforestry."
        },
        "Gold Standard": {
            "url": "https://www.goldstandard.org/donate-to-gold-standard",
            "description": "Gold Standard is a small Swiss-based NGO with a big impact. Established in 2003, Gold Standard projects have already prevented more than 300 million tonnes of CO2 from entering our atmosphere."
        }
    }
    
    for name, info in offset_links.items():
        st.write(f"[{name}]({info['url']})")
        st.write(info['description'])
        st.write("")  # Add a blank line for better spacing
