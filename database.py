import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
#conn2 = st.connection("gsheets2", type=GSheetsConnection)

df = conn.read()
#df2 = conn2.read()


st.write(df)
#st.write(df2)


data = {
    "UserID": "user123",
    "Quiz_Time": "2023-11-15 10:30:00",
    "diet": "Vegetarian",
    "food_waste": 50,
    "vehicle": "Car",
    "hours_in_vehicle": 2.5,
    "public_transport_hours": 1.0,
    "domestic_flights": 0,
    "indian_subcontinent_flights": 0,
    "international_flights": 1,
    "house_type": "Apartment",
    "cooling": "Air Conditioning",
    "home_improvements": 100,
    "new_items": 50,
    "non_essential_spending": 200,
    "offsetting_frequency": "Yearly",
    "offsetting_actions": "Carbon offsetting purchases"


conn.write(data)
df = conn.read()

st.write(df)
