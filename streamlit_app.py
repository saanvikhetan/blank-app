import streamlit as st


import streamlit as st

# Title of the app
st.title("Carbon Footprint Tracker")

st.header("Quiz: Calculate Your Carbon Footprint")
st.write("Answer the following questions to estimate your carbon footprint.")

# Section 1: Diet
st.subheader("Diet")
q1 = st.radio(
    "How would you best describe your diet?",
    ["Meat in every meal", "Meat in some meals", "Meat very rarely", "Vegetarian", "Vegan"],
)

q2 = st.radio(
    "In a week, how much do you spend on food from restaurants, canteens, and takeaways?",
    ["0", "1 - 2000", "2000 - 10000", "10000 and over"],
)

q3 = st.radio(
    "Of the food you buy, how much is wasted and thrown away?",
    ["None", "0% - 10%", "10% - 30%", "More than 30%"],
)

# Section 2: Travel
st.subheader("Travel")
q4 = st.radio(
    "Which of these best describes the vehicle you use most?",
    [
        "Electric car",
        "Hybrid car",
        "Small petrol or diesel car",
        "Medium petrol or diesel car",
        "Large petrol or diesel car",
        "Motorbike",
        "Neither - I walk, cycle or use public transport for all my journeys",
    ],
)

q5 = st.radio(
    "How many hours a week do you spend in your car or on your motorbike for personal use including commuting?",
    ["Under 2 hours", "2 to 5 hours", "5 to 15 hours", "15 to 25 hours", "Over 25 hours"],
)

q6 = st.radio(
    "How many hours a week do you spend on public transport (metro/train/bus) for personal use including commuting?",
    [
        "I don’t travel by metro/bus/train",
        "Under 2 hours",
        "2 to 5 hours",
        "5 to 15 hours",
        "15 to 25 hours",
        "Over 25 hours",
    ],
)

q7_domestic = st.slider(
    "In the last year, how many return flights have you made to domestic locations?", 0, 20, 0
)
q7_subcontinent = st.slider(
    "In the last year, how many return flights have you made to the Indian Subcontinent?", 0, 20, 0
)
q7_international = st.slider(
    "In the last year, how many return flights have you made to international locations?", 0, 20, 0
)

q8 = st.radio(
    "What percentage of your flights do you offset?",
    ["None of them", "25%", "50%", "75%", "All of them", "Not applicable"],
)

# Section 3: Home
st.subheader("Home")
q9 = st.radio(
    "What kind of house do you live in?",
    ["Detached", "Semi-detached", "Terrace", "Flat"],
)

q10 = st.radio(
    "How many bedrooms does your house have?",
    ["1", "2", "3", "4 or more"],
)

q11 = st.radio(
    "How many people (aged 17 and over) live in your house?",
    ["1", "2", "3", "4", "5 or more"],
)

q12 = st.radio(
    "How do you heat your home?",
    ["Gas", "Oil", "Electricity", "Wood", "Heatpump"],
)

q13 = st.radio(
    "Do you regularly turn off lights and not leave your appliances on standby?",
    ["Yes", "No"],
)

q14 = st.radio(
    "How cold do you keep your home in summer?",
    ["Below 19°C", "19 - 23°C", "24 - 30°C", "I don’t use an AC"],
)

# Submit Button
if st.button("Submit"):
    st.success("Thank you for completing the quiz! Your responses have been recorded.")

