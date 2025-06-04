import streamlit as st
import smtplib
import pandas as pd
import os
from google.cloud import firestore
# Initialize Firestore client
db = firestore.Client()

# Firestore collection name
LEADERBOARD_COLLECTION = "plastic_leaderboard"

def add_entry_to_firestore(entry):
    db.collection(LEADERBOARD_COLLECTION).add(entry)

def get_leaderboard_from_firestore():
    docs = db.collection(LEADERBOARD_COLLECTION).stream()
    leaderboard = []
    for doc in docs:
        leaderboard.append(doc.to_dict())
    return leaderboard
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
        # Define a CSV file to store leaderboard data
        LEADERBOARD_CSV = "leaderboard.csv"

        # Save leaderboard to CSV
        def save_leaderboard(leaderboard):
            df = pd.DataFrame(leaderboard)
            df.to_csv(LEADERBOARD_CSV, index=False)

        # Load leaderboard from CSV
        def load_leaderboard():
            if os.path.exists(LEADERBOARD_CSV):
                return pd.read_csv(LEADERBOARD_CSV).to_dict(orient="records")
            return []

        # On first run, load leaderboard from CSV
        if "loaded_leaderboard" not in st.session_state:
            st.session_state.leaderboard = load_leaderboard()
            st.session_state.loaded_leaderboard = True

        # Save leaderboard after new entry
        if st.session_state.leaderboard:
            save_leaderboard(st.session_state.leaderboard)
        # To make this app accessible to everyone, you need to deploy it to a public server.
        # Popular options include Streamlit Community Cloud (https://streamlit.io/cloud), Heroku, or any cloud VM.
        # Steps for Streamlit Community Cloud:
        # 1. Push this code to a public GitHub repository.
        # 2. Go to https://streamlit.io/cloud and sign in.
        # 3. Click "New app", select your repo and branch, and set the file path to Test.py.
        # 4. Deploy the app. Share the generated URL with others.

        st.info("To make this dashboard public, deploy it using Streamlit Community Cloud or another hosting service. All leaderboard entries will be visible to everyone accessing the app.")