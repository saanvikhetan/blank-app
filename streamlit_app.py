import streamlit as st

# Initialize session state variables
if "question_number" not in st.session_state:
    st.session_state.question_number = 1
if "responses" not in st.session_state:
    st.session_state.responses = []
if "final_score" not in st.session_state:
    st.session_state.final_score = None

# Questions and options
questions = [
    {"category": "DIET", "question": "How would you best describe your diet?", 
     "options": ["Meat in every meal", "Meat in some meals", "Meat very rarely", "Vegetarian", "Vegan"], 
     "scores": [3.3, 2.5, 1.7, 1.2, 0.9]},
    {"category": "DIET", "question": "Of the food you buy, how much is wasted and thrown away?", 
     "options": ["None", "0% - 10%", "10% - 30%", "More than 30%"], 
     "scores": [0, 0.1, 0.4, 1.0]},
    {"category": "TRAVEL", "question": "Which of these best describes the vehicle you use most?", 
     "options": ["Electric car", "Hybrid car", "Small petrol/diesel car", "Medium petrol/diesel car", 
                 "Large petrol/diesel car", "Motorbike", "Public Transport", "Neither - I walk or cycle for most of my journeys"], 
     "scores": [1, 2, 3, 4, 5, 3, 1.5, 0]},
    {"category": "TRAVEL", "question": "How many hours a week do you spend in your car or on your motorbike for personal use including commuting?", 
     "options": ["Under 2 hours", "2 to 5 hours", "5 to 15 hours", "15 to 25 hours", "Over 25 hours"], 
     "scores": [1, 2, 4, 6, 8]},
    {"category": "TRAVEL", "question": "How many hours a week do you spend on public transport (metro/train/bus) for personal use including commuting?", 
     "options": ["I don’t travel by metro/bus/train", "Under 2 hours", "2 to 5 hours", "5 to 15 hours", "15 to 25 hours", "Over 25 hours"], 
     "scores": [0, 0.5, 1, 1.5, 2, 2.5]},
    {"category": "TRAVEL", "question": "In the last year, how many return flights have you made in total to the following locations?",
     "options": ["Domestic (number of flights)", "Indian Subcontinent (number of flights)", "International (number of flights)"], 
     "input": True},
    {"category": "HOME", "question": "What kind of house do you live in?", 
     "options": ["Detached", "Semi-detached", "Terrace", "Flat"], 
     "scores": [6, 4, 3, 2]},
    {"category": "HOME", "question": "How cool is your house during summer?", 
     "options": ["I don’t use a cooler", "Below 19°C (very cold)", "19°C - 23°C (moderately cool)", "24°C - 30°C (energy-saving)"], 
     "scores": [0, 3, 2, 1]},
    {"category": "HOME", "question": "Which of these home energy efficiency improvements are installed in your home?", 
     "options": ["Energy-saving lightbulbs", "Loft insulation", "Cavity or solid wall insulation", "Condensing boiler", 
                 "Double glazing", "Low flow fittings to taps and showers", "Solar panels", "Solar water heater"], 
     "multi": True, "scores": -0.2},
    {"category": "STUFF", "question": "In the last 12 months, have you bought any of these new household items?", 
     "options": ["TV, laptop, or PC", "Large item of furniture", "Washing machine, dishwasher, etc.", "Mobile phone or tablet"], 
     "scores": [0.2, 0.3, 0.4, 0.1]},
    {"category": "STUFF", "question": "In a typical month, how much do you spend on non-essential items (clothes, grooming, entertainment, and pets)?", 
     "options": ["₹0 - ₹5,000", "₹5,000 - ₹15,000", "₹15,000 - ₹30,000", "Over ₹30,000"], 
     "scores": [0.2, 0.5, 1, 1.5]},
    {"category": "OFFSET", "question": "How often do you take actions to offset your carbon footprint?", 
     "options": ["I never take offsetting actions", "Rarely (once or twice a year)", "Sometimes (a few times a year)", 
                 "Often (monthly or more frequently)", "Always (I actively offset regularly and for most of my activities)"], 
     "scores": [0, -0.1, -0.3, -0.6, -1]},
    {"category": "OFFSET", "question": "What types of offsetting actions do you take?", 
     "options": ["Donate to environmental projects (tree planting, renewable energy, etc.)", 
                 "Participate in local initiatives (e.g., tree planting, clean-ups)", 
                 "Purchase carbon credits", "Other"], 
     "multi": True, "scores": [-0.2, -0.3, -0.2, 0]},
]

# Handle question logic
if st.session_state.final_score is None:
    question = questions[st.session_state.question_number - 1]
    st.subheader(f"{question['category']}: {question['question']}")
    if "input" in question and question["input"]:
        response = st.number_input("Enter number of flights for each category", min_value=0, step=1)
    elif "multi" in question and question["multi"]:
        response = st.multiselect("Select all that apply:", question["options"])
    else:
        response = st.radio("Select one:", question["options"])

    if st.button("Next"):
        st.session_state.responses.append(response)
        if st.session_state.question_number < len(questions):
            st.session_state.question_number += 1
        else:
            # Calculate the final score
            total_score = 0
            for i, resp in enumerate(st.session_state.responses):
                q = questions[i]
                if "input" in q and q["input"]:
                    total_score += resp * (0.5 if i == 5 else 3)
                elif "multi" in q and q["multi"]:
                    total_score += len(resp) * q["scores"]
                else:
                    total_score += q["scores"][q["options"].index(resp)]
            st.session_state.final_score = total_score
else:
    st.success(f"Your estimated annual carbon footprint is {st.session_state.final_score:.2f} tons CO₂e.")



