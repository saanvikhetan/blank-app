import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import users as user_lib
from datetime import date

# Custom CSS for styling
st.markdown("""
    <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 12px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stHeader, .stSubheader {
            color: #4CAF50;
        }
        .stSidebar .stSidebarContent {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 10px;
        }
        .stSidebar .stSidebarContent .stHeader {
            color: #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)

def update_carbon_footprint_history(new_value):
    st.session_state.carbon_footprint_history.append(new_value)

# --- Initialization of session state variables ---
if 'carbon_footprint_history' not in st.session_state:
    st.session_state.carbon_footprint_history = []

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
    "home_cooling": {
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
        "None": 0,
        "Spending": {
            "₹0 - ₹5,000": 0.2,
            "₹5,000 - ₹15,000": 0.5,
            "₹15,000 - ₹30,000": 1,
            "Over ₹30,000": 1.5,
        },
    },
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

def get_progress_level(points):
    for level in progress_levels:
        if level["points"][0] <= points <= level["points"][1]:
            return level
    return None

# --- Streamlit App ---
st.markdown("# 🌍 Carbon Footprint Calculator")

# Initialize session state for goals and points
if "goals" not in st.session_state:
    st.session_state.goals = []
if "eco_points" not in st.session_state:
    st.session_state.eco_points = 0
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False

# Navigation menu
if not user_lib.is_user_logged_in():
    user_lib.show_users_login()
    menu = None
elif st.session_state.quiz_completed:
    menu = st.radio("Navigation", ["Home", "Goals", "Offset", "Levels","Streaks"])
else:
    menu = "Quiz"
    
# Sidebar for displaying points and level
if user_lib.is_user_logged_in() and "eco_points" in st.session_state and st.session_state.quiz_completed:
    progress_level = get_progress_level(st.session_state.eco_points)
    if progress_level:
        st.sidebar.header("Your Progress")
        st.sidebar.write(f"**{progress_level['title']}**")
        st.sidebar.write(progress_level["description"])
        st.sidebar.write(f"Total Eco Points: {sum(goal['points'] for goal in st.session_state.completed_goals)}")
        st.sidebar.write(f"**Total Carbon Footprint:** {st.session_state.total_emissions:.2f} tons of CO₂e")


# --- Quiz Section ---
if user_lib.is_user_logged_in() and not st.session_state.quiz_completed:
    st.markdown("## 📝 Calculate Your Carbon Footprint")

    # --- DIET ---
    st.markdown("### 🍽️ Diet")
    diet = st.selectbox(
        "How would you best describe your diet?",
        list(emission_factors["diet"].keys())
    )
    food_waste = st.selectbox(
        "Of the food you buy, how much is wasted and thrown away?",
        list(emission_factors["food_waste"].keys())
    )

    # --- TRAVEL ---
    st.markdown("### 🚗 Travel")
    vehicle = st.selectbox(
        "Which of these best describes the mode of transport you use most?",
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
    st.markdown("### 🏡 Home")
    house_type = st.selectbox(
        "What kind of house do you live in?",
        list(emission_factors["home"].keys())
    )
    cooling = st.selectbox(
        "How cool is your house during summer?",
        list(emission_factors["home_cooling"].keys()),
    )

    # --- STUFF ---
    st.markdown("### 📦 Stuff")
    new_items = st.multiselect(
        "In the last 12 months, have you bought any of these new household items?",
        [
            "TV, laptop, or PC",
            "Washing machine, dishwasher, etc.",
            "Mobile phone or tablet",
            "None",
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
        cooling_emissions = emission_factors["home_cooling"][cooling]

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
        update_carbon_footprint_history(total_emissions)
        st.success(f"Your estimated annual carbon footprint is: {total_emissions:.2f} tons of CO₂e")

        # Pie Chart
        st.markdown("## 📊 Breakdown of Your Carbon Footprint")
        fig, ax = plt.subplots()
        labels = category_emissions.keys()
        sizes = category_emissions.values()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#FF9999", "#66B3FF", "#99FF99", "#FFCC99"])
        ax.axis('equal')
        st.pyplot(fig)

        # --- Bar Graph ---
        st.markdown("## 🌍 Comparison to Global Averages")
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
        st.markdown("## 🎯 Personalized Goals")

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

        st.markdown(f"### Weekly Goal for {max_category}")
        st.write(weekly_goals[max_category])

        st.markdown(f"### Daily Goal for {max_category}")
        st.write(daily_goals[max_category])

        # Mark quiz as completed
        st.session_state.quiz_completed = True

    # Add "Done" button to go to the home page
    if st.session_state.quiz_completed:
        if st.button("Done"):
            st.session_state.quiz_completed = True
            st.rerun()
            
# --- Streaks Section ---
if user_lib.is_user_logged_in() and menu == "Streaks":
    st.markdown("## 📅 Track Your Daily Eco-Friendly Streaks")

    # Define streak activities and their descriptions
    streaks = {
        "Donate an Unused Item": "Set aside something you no longer need for donation.",
        "Walk or Bike 1 Kilometer Instead of Driving": "Replace a short trip with walking or biking.",
        "Cook a Plant-Based Meal": "Prepare a vegetarian or vegan meal yourself.",
        "Conserve Water": "Turn off the tap while brushing your teeth or washing your hands.",
        "Plant Something": "Plant a seed, herb, or small tree in your garden or a pot."
    }

    # Display streak actions with checkboxes
    completed_tasks = 0
    for streak, description in streaks.items():
        col1, col2 = st.columns([1, 3])
        with col1:
            completed = st.checkbox("", value=st.session_state.streaks[streak], key=streak)
        with col2:
            st.markdown(f"**{streak}**: {description}")
        st.session_state.streaks[streak] = completed
        if completed:
            completed_tasks += 1

    # Get today's date
    today = date.today()

    # Logic for awarding points
    if st.session_state.last_streak_date != today:
        # New day: Reset daily streak logic
        st.session_state.last_streak_date = today
        st.session_state.bonus_given = False
        st.session_state.streak_counter = 0

        # Reset tasks for the new day
        for streak in streaks.keys():
            st.session_state.streaks[streak] = False

    # Award 1 streak point for completing at least one task
    if completed_tasks > 0 and st.session_state.streak_counter == 0:
        st.session_state.streak_points += 1
        st.session_state.streak_counter += 1

    # Award bonus points if all tasks are completed
    if completed_tasks == len(streaks) and not st.session_state.bonus_given:
        st.session_state.streak_points += 20
        st.session_state.bonus_given = True

    # Display streak points and task count
    st.markdown(f"### 🌟 Streak Points: {st.session_state.streak_points}")
    st.write(f"Completed Tasks Today: {completed_tasks}")
