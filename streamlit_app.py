import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Pie Chart and Suggestions ---
def calculate_emissions_breakdown():
    """Calculates emissions breakdown by category."""
    breakdown = {
        "Diet": emission_factors["diet"][diet] + emission_factors["food_waste"][food_waste],
        "Travel": (
            emission_factors["vehicle_use"][vehicle] * hours_in_vehicle
            + emission_factors["vehicle_use"]["Public Transport"] * public_transport_hours
            + domestic_flights * 0.5
            + indian_subcontinent_flights * 1.5
            + international_flights * 3
        ),
        "Home": (
            emission_factors["home"][house_type]
            + emission_factors["home"]["Cooling"][cooling]
            + emission_factors["home"]["Improvements"] * len(home_improvements)
        ),
        "Stuff": (
            sum(emission_factors["stuff"][item] for item in new_items)
            + emission_factors["stuff"]["Spending"][non_essential_spending]
        ),
    }
    offsetting_reductions = (
        emission_factors["offsetting"]["Frequency"][offsetting_frequency]
        + sum(emission_factors["offsetting"]["Actions"].get(action, 0) for action in offsetting_actions)
    )
    breakdown["Offsetting"] = offsetting_reductions
    return breakdown

def display_pie_chart(breakdown):
    """Displays a pie chart of the emissions breakdown."""
    categories = list(breakdown.keys())
    emissions = [value for value in breakdown.values()]

    fig, ax = plt.subplots()
    ax.pie(emissions, labels=categories, autopct="%1.1f%%", startangle=140)
    ax.set_title("Carbon Footprint Breakdown by Category")
    st.pyplot(fig)

def generate_suggestions(breakdown):
    """Generates personalized suggestions based on the highest-emitting category."""
    highest_category = max(breakdown, key=breakdown.get)

    suggestions = {
        "Diet": (
            "It seems your diet choices contribute significantly to your carbon footprint. "
            "Consider reducing meat consumption, wasting less food, and trying plant-based alternatives."
        ),
        "Travel": (
            "Your travel habits are a major contributor. Try using public transport, carpooling, cycling, or walking when possible. "
            "Reduce air travel by taking fewer flights or exploring local holiday destinations."
        ),
        "Home": (
            "Your home energy use is a key contributor. Improve insulation, switch to energy-efficient appliances, and consider renewable energy options like solar panels."
        ),
        "Stuff": (
            "Your spending on non-essential items is contributing to your footprint. Consider buying fewer new items, opting for second-hand, or focusing on quality over quantity."
        ),
        "Offsetting": (
            "You're already taking steps to offset your carbon footprint. Continue supporting environmental projects and initiatives!"
        ),
    }

    st.markdown(f"**Suggestion:** {suggestions[highest_category]}")

# --- Display Results ---
if st.button("Calculate"):
    emissions_breakdown = calculate_emissions_breakdown()
    total_emissions = sum(emissions_breakdown.values())

    st.success(f"Your estimated annual carbon footprint is: {total_emissions:.2f} tons of CO₂e")
    st.header("Emissions Breakdown")
    display_pie_chart(emissions_breakdown)
    generate_suggestions(emissions_breakdown)

# --- Additional Information ---
st.markdown(
    """
    **Note:** This is a simplified estimation and may not reflect your actual carbon footprint accurately. 
    Consider consulting with a carbon footprint specialist for a more precise assessment.
    """
)
