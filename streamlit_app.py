import streamlit as st


# Initialize session state
if "question_number" not in st.session_state:
    st.session_state.question_number = 1
if "responses" not in st.session_state:
    st.session_state.responses = []

# Questions and options
questions = [
    {
        "question": "How would you best describe your diet?",
        "options": ["Meat in every meal", "Meat in some meals", "Meat very rarely", "Vegetarian", "Vegan"],
    },
    {
        "question": "In a week, how much do you spend on food from restaurants, canteens, and takeaways?",
        "options": ["0", "1 - 2000", "2000 - 10000", "10000 and over"],
    },
    {
        "question": "Of the food you buy, how much is wasted and thrown away?",
        "options": ["None", "0% - 10%", "10% - 30%", "More than 30%"],
    },
    {
        "question": "Which of these best describes the vehicle you use most?",
        "options": [
            "Electric car",
            "Hybrid car",
            "Small petrol or diesel car",
            "Medium petrol or diesel car",
            "Large petrol or diesel car",
            "Motorbike",
            "Neither - I walk, cycle or use public transport for all my journeys",
        ],
    },
    {
        "question": "How many hours a week do you spend in your car or on your motorbike for personal use including commuting?",
        "options": ["Under 2 hours", "2 to 5 hours", "5 to 15 hours", "15 to 25 hours", "Over 25 hours"],
    },
    # Add more questions here...
]

# Display current question
current_question_index = st.session_state.question_number - 1
question_data = questions[current_question_index]
st.subheader(f"Question {st.session_state.question_number}")
response = st.radio(question_data["question"], question_data["options"])

# Button to proceed to the next question
if st.button("Next"):
    st.session_state.responses.append(response)  # Save the response
    if st.session_state.question_number < len(questions):
        st.session_state.question_number += 1  # Move to the next question
    else:
        st.write("Thank you for completing the quiz!")
        st.write("Your responses:")
        for i, ans in enumerate(st.session_state.responses, start=1):
            st.write(f"Q{i}: {ans}")
        # Optionally reset the quiz
        if st.button("Restart Quiz"):
            st.session_state.question_number = 1
            st.session_state.responses = []

