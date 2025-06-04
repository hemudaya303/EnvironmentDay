import streamlit as st
import smtplib

st.title("Welcome to My Streamlit App")
st.write("This is a simple Streamlit application.")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")
    st.header("Plastic Consumption Calculator")

    # Define products and their average weights (in grams)
    products = {
        "Plastic Water Bottle": 20,
        "Plastic food container": 50,
        "Plastic bags": 6,
        "Wrap Materials (Groceries, Electronics)": 5,
        "Plastic Cup": 10,
        "Dustbin Covers and disposable bags": 5,
        "Food and Beverage Wrapper": 6
    }

    st.subheader("Enter your daily usage for each product:")

    # Collect user input for each product
    usage = {}
    for product, weight in products.items():
        usage[product] = st.number_input(
            f"How many {product}s do you use per day? (average weight: {weight}g)", min_value=0, step=1, key=product
        )

        # Calculate total plastic consumed per day
        total_per_day = sum(usage.get(prod, 0) * products[prod] for prod in products)

    total_per_year = total_per_day * 365

    st.markdown(f"**Average plastic consumed per day:** {total_per_day:.2f} grams")
    st.markdown(f"**Average plastic consumed per year:** {total_per_year:.2f} grams")
    st.markdown(f"**Average plastic consumed per year:** {total_per_year / 1000:.2f} kg")

    # Initialize session state to store leaderboard data
    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = []

    # Add current user's data to leaderboard if not already added
    if st.button("Submit and Add to Leaderboard"):
        entry = {
            "name": name,
            "per_day": total_per_day,
            "per_year": total_per_year,
            "per_year_kg": total_per_year / 1000
        }
        st.session_state.leaderboard.append(entry)
        st.success("Your data has been added to the leaderboard!")

    # Display the leaderboard
    if st.session_state.leaderboard:
        st.header("Plastic Consumption Leaderboard")
        # Sort by per_year_kg descending (highest consumption first)
        sorted_leaderboard = sorted(
            st.session_state.leaderboard, key=lambda x: x["per_year_kg"], reverse=True
        )
        st.table([
            {
                "Name": entry["name"],
                "Per Day (g)": f"{entry['per_day']:.2f}",
                "Per Year (g)": f"{entry['per_year']:.2f}",
                "Per Year (kg)": f"{entry['per_year_kg']:.2f}"
            }
            for entry in sorted_leaderboard
        ])
