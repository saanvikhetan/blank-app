import streamlit as st

# Initialize session state
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "responses" not in st.session_state:
    st.session_state.responses = []

# Questions and Options
questions = [
    {
        "question": "How would you best describe your diet?",
        "options": ["Meat in every meal", "Meat in some meals", "Meat very rarely", "Vegetarian", "Vegan"]
    },
    {
        "question": "Of the food you buy, how much is wasted and thrown away?",
        "options": ["None", "0% - 10%", "10% - 30%", "More than 30%"]
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
            "Neither - I walk or cycle for most of my journeys"
        ]
    },
    {
        "question": "How many hours a week do you spend in your car or on your motorbike for personal use including commuting?",
        "options": ["Under 2 hours", "2 to 5 hours", "5 to 15 hours", "15 to 25 hours", "Over 25 hours"]
    },
    {
        "question": "How many hours a week do you spend on public transport (metro/train/bus) for personal use including commuting?",
        "options": [
            "I don’t travel by metro/bus/train",
            "Under 2 hours",
            "2 to 5 hours",
            "5 to 15 hours",
            "15 to 25 hours",
            "Over 25 hours"
        ]
    },
    {
        "question": "In the last year, how many return flights have you made in total to the following locations? (Domestic, Subcontinent, International)",
        "options": ["Input your numbers below"]
    },
    {
        "question": "What kind of house do you live in?",
        "options": ["Detached", "Semi-detached", "Terrace", "Flat"]
    },
    {
        "question": "How cool is your house during summer?",
        "options": [
            "I don’t use a cooler",
            "Below 19°C (very cold)",
            "19°C - 23°C (moderately cool)",
            "24°C - 30°C (energy-saving)"
        ]
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
            "Solar water heater"
        ]
    },
    {
        "question": "In the last 12 months, have you bought any of these new household items?",
        "options": [
            "TV, laptop, or PC",
            "Large item of furniture",
            "Washing machine, dishwasher, etc.",
            "Mobile phone or tablet"
        ]
    },
    {
        "question": "In a typical month, how much do you spend on non-essential items (clothes, grooming, entertainment, and pets)?",
        "options": [
            "₹0 - ₹5,000",
            "₹5,000 - ₹15,000",
            "₹15,000 - ₹30,000",
            "Over ₹30,000"
        ]
    },
    {
        "question": "How often do you take actions to offset your carbon footprint?",
        "options": [
            "I never take offsetting actions",
            "Rarely (once or twice a year)",
            "Sometimes (a few times a year)",
            "Often (monthly or more frequently)",
            "Always (I actively offset regularly and for most of my activities)"
        ]
    }
]

# Display Current Question
question_index = st.session_state.current_question
if question_index < len(questions):
    question = questions[question_index]
    st.write(f"**{question['question']}**")

    # Display options or inputs based on the question
    if question_index == 5:  # Special case for flight input
        domestic = st.number_input("Domestic flights", min_value=0, step=1)
        subcontinent = st.number_input("Subcontinent flights", min_value=0, step=1)
        international = st.number_input("International flights", min_value=0, step=1)
        response = [domestic, subcontinent, international]
    else:
        response = st.radio("Select one:", question["options"])

    if st.button("Next"):
        st.session_state.responses.append(response)
        st.session_state.current_question += 1
else:
    # Show Results
    st.write("Thank you for completing the quiz!")
    st.write("Your Responses:")
    st.write(st.session_state.responses)



