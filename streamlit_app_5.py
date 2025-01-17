import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import user_lib

# --- Initialize Session State ---
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'completed_goals' not in st.session_state:
    st.session_state.completed_goals = []
if "total_emissions" not in st.session_state:
    st.session_state.total_emissions = 0

def mark_goal_as_completed(goal):
    if goal not in st.session_state.completed_goals:
        st.session_state.completed_goals.append(goal)
        st.session_state.total_emissions -= goal['carbon_reduction']  # Decrease emissions
        update_carbon_footprint_history(st.session_state.total_emissions)
    if goal in st.session_state.goals:
        st.session_state.goals.remove(goal)

# --- Main Interface ---
if user_lib.is_user_logged_in() and menu == "Goals":
    st.header("🌍 Set and Track Your Goals 🌿")

    # Flat list of goals
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

    # Filter out completed or already added goals
    added_actions = [goal["action"] for goal in st.session_state.completed_goals + st.session_state.goals]
    available_actions = [
        action for action in available_actions
        if action["action"] not in added_actions
    ]

    # Category Selection
    selected_category = st.selectbox("Choose a category:", list(goals_data.keys()), key="category_select")
    category_actions = [a for a in available_actions if a["category"] == selected_category]
    selected_action = st.selectbox("Choose an action to add to your goals:", [a["action"] for a in category_actions], key="action_select")

    if st.button("Add to Goals", key="add_goal_button"):
        action_to_add = next((a for a in category_actions if a["action"] == selected_action), None)
        if action_to_add and action_to_add not in st.session_state.goals:
            st.session_state.goals.append(action_to_add)
            st.success(f"✅ Added '{selected_action}' to your goals!")
        elif action_to_add:
            st.warning(f"⚠️ '{selected_action}' is already in your goals.")

    # Display Current Goals
    if st.session_state.goals:
        st.subheader("🔹 Your Current Goals")
        for i, goal in enumerate(st.session_state.goals):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"• {goal['action']} ({goal['category']}, +{goal['points']} points)")
            with col2:
                if st.button(f"Mark as Completed", key=f"complete_{i}", on_click=mark_goal_as_completed, args=(goal,)):
                    st.experimental_rerun()

    # Completed Goals
    if st.session_state.completed_goals:
        st.subheader("🏆 Completed Goals")
        for goal in st.session_state.completed_goals:
            st.markdown(f"<p style='color:green;'>• {goal['action']} (+{goal['points']} points)</p>", unsafe_allow_html=True)
        st.write(f"Total Eco Points: **{sum(goal['points'] for goal in st.session_state.completed_goals)}**")

    # Total Eco Points Display
    total_points = sum(goal['points'] for goal in st.session_state.goals) + sum(goal['points'] for goal in st.session_state.completed_goals)
    st.session_state.eco_points = total_points
    st.write(f"🌱 **Total Eco Points**: {total_points}")

# --- Offset Section ---
if user_lib.is_user_logged_in() and menu == "Offset":
    st.header("🌍 Offset Your Carbon Footprint 🌿")

    offset_links = {
        "HelpUsGreen": {
            "url": "https://www.helpusgreen.com/",
            "description": "By upcycling discarded temple flowers, they craft luxurious, eco-friendly incense. Therefore, fostering community growth and environmental conservation."
        },
        "Grow Trees": {
            "url": "https://www.grow-trees.com/index.php",
            "description": "With 20 million trees planted over almost 150 projects, Grow Trees is an environmental organization dedicated to facilitating tree planting through online platforms."
        },
        "Solar Aid": {
            "url": "https://solar-aid.org/",
            "description": "Using solar power light helps reduce the impact of toxic fumes from kerosene lamps and provides a sustainable change."
        },
        "TNC India": {
            "url": "https://www.tncindia.in/what-we-do/our-priorities/support-renewable-energy/",
            "description": "Their aim is to increase the use of climate solutions such as reforestation and clean energy transitions."
        },
        "WWF India": {
            "url": "https://join.wwfindia.org/?source=WWF-JOIN-WEB&utm_source=main_website&utm_medium=nav_link&utm_campaign=donate",
            "description": "WWF India focuses on improving environmental literacy, preserving wildlife, and promoting sustainable living."
        },
        "BJSM": {
            "url": "https://bjsm.org.in/donations/donate-to-protect-the-environment/",
            "description": "BJSM focuses on combating climate change, promoting sustainable land management, and agroforestry."
        },
        "Gold Standard": {
            "url": "https://www.goldstandard.org/donate-to-gold-standard",
            "description": "Gold Standard has helped prevent over 300 million tonnes of CO2 through various environmental projects."
        }
    }

    for name, info in offset_links.items():
        st.write(f"🌱 [**{name}**]({info['url']})")
        st.write(f"📝 {info['description']}")

# --- Levels Section ---
if user_lib.is_user_logged_in() and menu == "Levels":
    st.header("🏅 Available Levels 🎯")

    # Get the user's current progress level
    current_level = get_progress_level(st.session_state.eco_points)

    for level in progress_levels:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader(f"🎖️ {level['title']}")
            st.write(f"Points: {level['points'][0]} - {level['points'][1]}")
        with col2:
            if level == current_level:
                st.markdown("<p style='color:green;'>**This is you!**</p>", unsafe_allow_html=True)

        if st.button(f"Learn more about {level['title']}", key=level["title"]):
            st.write(level["description"])

