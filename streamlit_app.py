import streamlit as st

# Initialize session state
if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "responses" not in st.session_state:
    st.session_state.responses = []

if "final_footprint" not in st.session_state:
    st.session_state.final_footprint = 0

# Questions and options
questions = [
    {
        "question": "How would you best describe your diet?",
        "options": ["Meat in every meal", "Meat in some meals", "Meat very rarely", "Vegetarian", "Vegan"],
        "emissions": [3.3, 2.5, 1.7, 1.2, 0.9],
    },
    {
        "question": "Of the food you buy, how much is wasted and thrown away?",
        "options": ["None", "0% - 10%", "10% - 30%", "More than 30%"],
        "emissions": [0, 0.1, 0.4, 1.0],
    },
    {
        "question": "Which of these best describes the vehicle you use most?",
        "options": [
            "Electric car",
            "Hybrid car",
            "Small petrol/diesel car",
            "Medium petrol/diesel car",
            "Large petrol/diesel car",
            "Motorbike",
            "Public Transport",
            "Neither - I walk or cycle for most of my journeys",
        ],
        "emissions": [1, 2, 3, 4, 5, 2, 1.5, 0],
    },
    {
        "question": "How many hours a week do you spend in your car or on your motorbike for personal use including commuting?",
        "options": ["Under 2 hours", "2 to 5 hours", "5 to 15 hours", "15 to 25 hours", "Over 25 hours"],
        "emissions": [0.5, 1, 2.5, 4, 6],
    },
    {
        "question": "How many hours a week do you spend on public transport (metro/train/bus) for personal use including commuting?",
        "options": [
            "I don’t travel by metro/bus/train",
            "Under 2 hours",
            "2 to 5 hours",
            "5 to 15 hours",
            "15 to 25 hours",
            "Over 25 hours",
        ],
        "emissions": [0, 0.2, 0.5, 1.5, 2.5, 4],
    },
    {
        "question": "In the last year, how many return flights have you made in total to the following locations?\nDomestic (number of flights):",
        "type": "input",
        "emissions_per_unit": 0.5,
    },
    {
        "question": "In the last year, how many return flights have you made in total to the following locations?\nIndian Subcontinent (number of flights):",
        "type": "input",
        "emissions_per_unit": 1.5,
    },
    {
        "question": "In the last year, how many return flights have you made in total to the following locations?\nInternational (number of flights):",
        "type": "input",
        "emissions_per_unit": 3.0,
    },
    {
        "question": "What kind of house do you live in?",
        "options": ["Detached", "Semi-detached", "Terrace", "Flat"],
        "emissions": [6, 4, 3, 2],
    },
    {
        "question": "How cool is your house during summer?",
        "options": [
            "I don’t use a cooler",
            "Below 19°C (very cold)",
            "19°C - 23°C (moderately cool)",
            "24°C - 30°C (energy-saving)",
        ],
        "emissions": [0, 3, 2, 1],
    },
    {
        "question": "Which of these home energy efficiency improvements are installed in your home?",
        "options": [
            "Energy-saving lightbulbs",
            "Loft insulation",
            "Cavity or solid wall insulation",
            "Condensing boiler",
            "Double glazing",
            "Low flow fittings to taps and showers",
            "Solar panels",
            "Solar water heater",
        ],
        "emissions_reduction": 0.2,
    },
    {
        "question": "In a typical month, how much do you spend on non-essential items (clothes, grooming, entertainment, and pets)?",
        "options": ["₹0 - ₹5,000", "₹5,000 - ₹15,000", "₹15,000 - ₹30,000", "Over ₹30,000"],
        "emissions": [0.2, 0.5, 1, 1.5],
    },
]

# Display current question
current_question = questions[st.session_state.question_number - 1]

st.title("Carbon Footprint Quiz")

# Handle input types
if "options" in current_question:
    selected_option = st.radio(current_question["question"], current_question["options"])
    if st.button("Next"):
        index = current_question["options"].index(selected_option)
        st.session_state.responses.append(current_question["emissions"][index])
        st.session_state.question_number += 1
        st.experimental_rerun()
elif "type" in current_question and current_question["type"] == "input":
    user_input = st.number_input(current_question["question"], min_value=0, step=1)
    if st.button("Next"):
        st.session_state.responses.append(user_input * current_question["emissions_per_unit"])
        st.session_state.question_number += 1
        st.experimental_rerun()

# Calculate total emissions
if st.session_state.question_number > len(questions):
    total_emissions = sum(st.session_state.responses)
    st.header(f"Your total annual carbon footprint is: {total_emissions:.2f} tons CO₂e")
    st.session_state.final_footprint = total_emissions


