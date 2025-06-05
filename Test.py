import streamlit as st
import pandas as pd
import sqlite3
import os
# import plotly.express as px

DB_FILE = "leaderboard.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            per_day REAL NOT NULL,
            per_year REAL NOT NULL,
            per_year_kg REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_entry(username, entry):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO leaderboard (username, name, per_day, per_year, per_year_kg)
        VALUES (?, ?, ?, ?, ?)
    """, (username, entry["name"], entry["per_day"], entry["per_year"], entry["per_year_kg"]))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, username, name, per_day, per_year, per_year_kg FROM leaderboard")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_entry(entry_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM leaderboard WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

init_db()

st.title("Plastic Consumption Tracker")
username = st.text_input("Enter your username to login")
if username:
    name = st.text_input("Enter your name:")
    if name:
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

        usage = {}
        for product, weight in products.items():
            usage[product] = st.number_input(f"{product} (avg weight: {weight}g)", min_value=0, step=1)

        total_per_day = sum(usage[p] * products[p] for p in usage)
        total_per_year = total_per_day * 365
        total_per_year_kg = total_per_year / 1000

        st.write(f"Daily: {total_per_day:.2f}g, Yearly: {total_per_year:.2f}g / {total_per_year_kg:.2f}kg")

        if st.button("Submit"):
            add_entry(username, {"name": name, "per_day": total_per_day,
                                 "per_year": total_per_year, "per_year_kg": total_per_year_kg})
            st.success("Entry added!")

    st.subheader("Leaderboard")
    data = get_leaderboard()
    df = pd.DataFrame(data, columns=["ID", "Username", "Name", "Per Day", "Per Year", "Per Year (kg)"])
    st.dataframe(df)

    # if st.button("Show Chart"):
    #     fig = px.bar(df, x="Name", y="Per Year (kg)", color="Name", title="Plastic Usage per Year (kg)")
    #     st.plotly_chart(fig)

    delete_id = st.number_input("Enter ID to delete", step=1, min_value=1)
    if st.button("Delete Entry"):
        delete_entry(delete_id)
        st.success("Entry deleted. Please refresh.")

    st.info("For database sync, upload/download the file 'leaderboard.db' to/from your Google Drive manually.")
    st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #a8e063 0%, #56ab2f 100%);
        color: #222;
    }
    .stApp {
        background: linear-gradient(135deg, #a8e063 0%, #56ab2f 100%);
    }
    .css-18e3th9 {
        background: rgba(255,255,255,0.8);
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
        <div>
            <h2 style="color:#22543d;margin-bottom:0;">Green Energy Plastic Tracker</h2>
            <p style="color:#22543d;font-weight:bold;">Powered by Acies Global</p>
        </div>
        <img src="https://aciesglobal.com/wp-content/uploads/2022/06/Acies-Logo.png" alt="Acies Global" height="60">
    </div>
    """,
    unsafe_allow_html=True
)
