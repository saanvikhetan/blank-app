import streamlit as st

# Initialize session state
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# Questions and options
questions = [
    {
        "category": "DIET",
        "question": "How would you best describe your diet?",
        "options": ["Meat in every meal", "Meat in some meals", "Meat very rarely", "Vegetarian", "Vegan"],
        "values": [3.3, 2.5, 1.7, 1.2, 0.9],
    },
    {
        "category": "DIET",
        "question": "Of the food you buy, how much is wasted and thrown away?",
        "options": ["None", "0% - 10%", "10% - 30%", "More than 30%"],
        "values": [0, 0.1, 0.4, 1.0],
    },
    {
        "category": "TRAVEL",
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
        "values": [1, 2, 3, 4, 5, 2, 1.5, 0],
    },
    {
        "category": "TRAVEL",
        "question": "In the last year, how many return flights have you made in total to the following locations?",
        "options": ["Domestic", "Indian Subcontinent", "International"],
        "values": [0.5, 1.5, 3],
        "type": "input",
    },
    {
        "category": "HOME",
        "question": "What kind of house do you live in?",
        "options": ["Detached", "Semi-detached", "Terrace", "Flat"],
        "values": [6, 4, 3, 2],
    },
    {
        "category": "STUFF",
        "question": "In the last 12 months, have you bought any of these new household items?",
        "options": [
            "TV, laptop, or PC",
            "Large item of furniture",
            "Washing machine, dishwasher, etc.",
            "Mobile phone or tablet",
        ],
        "values": [0.2, 0.3, 0.4, 0.1],
        "type": "multi",
    },
    {
        "category": "OFFSET",
        "question": "How often do you take actions to offset your carbon footprint?",
        "options": [
            "I never take offsetting actions",
            "Rarely (once or twice a year)",
            "Sometimes (a few times a year)",
            "Often (monthly or more frequently)",
            "Always (I actively offset regularly and for most of my activities)",
        ],
        "values": [0, -0.1, -0.3, -0.6, -1],
    },
]

# Display question
question_index = st.session_state.question_index
if question_index < len(questions):
    question_data = questions[question_index]
    st.write(f"### {question_data['category']}: {question_data['question']}")

    if question_data.get("type") == "input":
        responses = []
        for option in question_data["options"]:
            response = st.number_input(f"{option} (number of flights):", min_value=0, step=1, key=f"{option}_input")
            responses.append(response)
        if st.button("Next"):
            st.session_state.responses[question_data["category"]] = responses
            st.session_state.question_index += 1
            st.experimental_rerun()

    elif question_data.get("type") == "multi":
        response = st.multiselect(
            "Select all that apply:",
            options=question_data["options"],
            key=f"multi_{question_index}"
        )
        if st.button("Next"):
            st.session_state.responses[question_data["category"]] = response
            st.session_state.question_index += 1
            st.experimental_rerun()

    else:
        response = st.radio(
            "Select one:",
            options=question_data["options"],
            key=f"radio_{question_index}"
        )
        if st.button("Next"):
            st.session_state.responses[question_data["category"]] = response
            st.session_state.question_index += 1
            st.experimental_rerun()

else:
    # Calculate carbon footprint
    total_emissions = 0

    # Map responses to values
    for i, question in enumerate(questions):
        category = question["category"]
        if category not in st.session_state.responses:
            continue

        response = st.session_state.responses[category]

        if question.get("type") == "input":
            for j, val in enumerate(response):
                total_emissions += val * question["values"][j]
        elif question.get("type") == "multi":
            for item in response:
                total_emissions += question["values"][question["options"].index(item)]
        else:
            total_emissions += question["values"][question["options"].index(response)]

    st.write(f"## Your Total Annual Carbon Footprint: {total_emissions:.2f} tons CO₂e")

    # Reset option
    if st.button("Restart Quiz"):
        st.session_state.question_index = 0
        st.session_state.responses = {}
        st.experimental_rerun()



