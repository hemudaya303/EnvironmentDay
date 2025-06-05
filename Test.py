import streamlit as st
import pandas as pd
import sqlite3
import base64

# -------------------- INIT DB --------------------
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

def delete_entry():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM leaderboard")
    conn.commit()
    conn.close()

def get_base64_image(image_path):
    """Convert image to base64 string for embedding in HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Plastic Consumption Tracker", layout="wide")

# Get logo image as base64
logo_base64 = get_base64_image("Logo.png")

# -------------------- STYLING --------------------
st.markdown(f"""
    <style>
    /* Remove default Streamlit padding and margins */
    .main .block-container {{
        padding-top: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }}
    
    /* Background styling */
    .stApp {{
        background-color: #e6ffe6;
    }}
    
    /* Fixed header - positioned below Streamlit's deploy header */
    .header {{
        background-color: #2e7d32;
        padding: 15px 30px;
        border-radius: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 2.875rem;  /* Position below Streamlit's header */
        left: 0;
        right: 0;
        width: 100%;
        z-index: 999;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        box-sizing: border-box;
    }}
    
    .header-left {{
        display: flex;
        align-items: center;
    }}
    
    .header img {{
        height: 40px;
        margin-right: 10px;
        border-radius: 0px;
    }}
    
    .header h2 {{
        color: white;
        margin: 0;
        font-size: 36px;
        font-weight: bold;
    }}
    
        /* Force all visible text elements to be black for dark mode compatibility */
    * {{
        color: #000000 !important;
    }}
    .stApp, .main, .block-container, .stTextInput, .stNumberInput, .markdown-text-container, .stMarkdown, .stMarkdown p, .stMarkdown div {{
        color: #000000 !important;
    }}
    .stDataFrame div {{
        color: #ffffff !important;
    }}
    input, textarea, select {{
        color: #000000 !important;
    }}
    
    
    /* Main container with proper spacing for fixed header */
    .container {{
        max-width: 70%;
        margin: 10px auto 10px auto;  /* Reduced top margin to eliminate white space */
        padding: 30px;
        border-radius: 10px;
        width: 70%;
    }}
    
    /* Button styling */
    .custom-btn {{
        background-color: #2e7d32;
        color: white;
        padding: 0.5em 1.5em;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }}
    
    .custom-btn:hover {{
        background-color: #60ad5e;
    }}
    
    /* Streamlit button styling */
    .stButton > button {{
        background-color: #2e7d32;
        color: white;
        border: none;
        padding: 0.5em 1.5em;
        border-radius: 5px;
        font-weight: bold;
    }}
    
    .stButton > button:hover {{
        background-color: #60ad5e;
        border: none;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f8f0;
        border-radius: 8px 8px 0px 0px;
        gap: 10px;
        padding-left: 20px;
        padding-right: 20px;
        color: #2e7d32;
        font-weight: bold;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: #2e7d32;
        color: white;
    }}
    
    /* Input field styling */
    .stTextInput > div > div > input {{
        border: 2px solid #2e7d32;
        border-radius: 5px;
        padding: 10px;
        background-color: white;
    }}
    
    .stNumberInput > div > div > input {{
        border: 2px solid #2e7d32;
        border-radius: 5px;
        padding: 10px;
        background-color: white;
    }}
    
    /* Metrics and text styling */
    h1, h2, h3, h4 {{
        color: #2e7d32;
    }}
    
    /* Dataframe styling */
    .stDataFrame {{
        border: 1px solid #2e7d32;
        border-radius: 5px;
    }}
    
    /* Image styling */
    .stImage {{
        border-radius: 10px;
    }}
    
    /* Success/Warning/Info message styling */
    .stSuccess {{
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
    }}
    
    .stWarning {{
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
    }}
            

    /* Green border for number input */
    input[type="number"] {{
        border: 2px solid #2e7d32 !important;
        border-radius: 5px;
        padding: 5px;
        background-color: white;
    }}

    
    .stInfo {{
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
    }}
    </style>

    <div class="header">
        <div class="header-left">
            {"" if not logo_base64 else f'<img src="data:image/png;base64,{logo_base64}" alt="Logo">'}
            <h2>Plastic Consumption Tracker</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

# -------------------- APP START --------------------
init_db()

# Session State
if "name_entered" not in st.session_state:
    st.session_state.name_entered = False
# if "show_leaderboard" not in st.session_state:
#     st.session_state.show_leaderboard = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# -------------------- BODY --------------------
with st.container():
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Intro section: Text + Image
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        
        #### Why It Matters:
        **Plastic pollution is one of the most urgent environmental challenges of our time**, with over 350 million tonnes of plastic waste generated globally every year and millions of tonnes leaking into our land and oceans.

        This pollution **threatens wildlife**, **contaminates ecosystems**, and **even impacts human health**, as plastics can take centuries to decompose and often break down into harmful microplastics.

        As we mark World Environment Day, it's clear that **collective action is needed to #BeatPlasticPollution**.

        By making small changes like using **reusable bottles and bags**, avoiding **single-use plastics**, and choosing **products with less packaging** we can each reduce our plastic footprint and help protect the planet for future generations.

        🌍 **Your journey to track and cut down plastic consumption starts here — every choice counts!**
        """)
    with col2:
        st.image("bottle.png", use_container_width=True)

    # Name input
    if not st.session_state.name_entered:
        st.markdown("""
            <div style='text-align: center; padding-top: 20px;'>
                <h3 style='color: black;'>Enter Your Name to Begin</h3>
            </div>
        """, unsafe_allow_html=True)

        # Centered input box inside a column layout
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            name_input = st.text_input("Your Name", label_visibility="collapsed", key="centered_name_input")
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if st.button("Enter Name", key="enter_name_btn"):
                if name_input.strip() != "":
                    st.session_state.user_name = name_input.strip()
                    st.session_state.name_entered = True
                    st.rerun()
                else:
                    st.warning("Please enter a valid name.")


    # -------------------- TABS --------------------
    if st.session_state.name_entered:
        tab1, tab2 = st.tabs(["📝 Input Tracker", "🏆 Leaderboard"])

        with tab1:
            st.subheader(f"Hello {st.session_state.user_name}, enter your daily usage:")

            products = {
                "Plastic Water Bottle": 20,
                "Plastic food container": 50,
                "Plastic bags": 6,
                "Wrap Materials (Groceries, Electronics)": 5,
                "Plastic Cup": 10,
                "Dustbin Covers and disposable bags": 5,
                "Food and Beverage Wrapper": 6
            }

            usage = {}
            for product, weight in products.items():
                usage[product] = st.number_input(f"{product} (avg weight: {weight}g)", min_value=0, step=1)

            total_per_day = sum(usage[p] * products[p] for p in usage)
            total_per_year = total_per_day * 365
            total_per_year_kg = total_per_year / 1000

            st.write(f"**Daily Usage:** {total_per_day:.2f}g")
            st.write(f"**Yearly Usage:** {total_per_year:.2f}g / {total_per_year_kg:.2f}kg")

            if st.button("Submit"):
                add_entry(
                    username=st.session_state.user_name.lower().replace(" ", "_"),
                    entry={
                        "name": st.session_state.user_name,
                        "per_day": total_per_day,
                        "per_year": total_per_year,
                        "per_year_kg": total_per_year_kg
                    }
                )
                st.success("Entry added!")
                st.session_state.show_leaderboard = True

        with tab2:
            if st.session_state.show_leaderboard:
                st.subheader("🏆 Leaderboard")
                data = get_leaderboard()
                df = pd.DataFrame(data, columns=["ID", "Username", "Name", "Per Day", "Per Year", "Per Year (kg)"])
                st.dataframe(df, use_container_width=True)

    if st.button("Delete Entry"):
        delete_entry()
        st.success("Entry deleted. Please refresh.")

    # st.markdown(
    #     """
    #     <style>
    #     .header-container {
    #         display: flex;
    #         align-items: flex-start;
    #         justify-content: space-between;
    #         margin-bottom: 20px;
    #     }
    #     .logo-left {
    #         flex: 0 0 auto;
    #         margin-right: 20px;
    #     }
    #     .title-right {
    #         flex: 1 1 auto;
    #         text-align: right;
    #     }
    #     .leaderboard-container {
    #         display: flex;
    #         justify-content: flex-end;
    #         margin-top: 30px;
    #     }
    #     </style>
    #     <div class="header-container">
    #         <div class="logo-left">
    #             <img src="https://aciesglobal.com/wp-content/uploads/2022/06/Acies-Logo.png" alt="Acies Global" height="60">
    #         </div>
    #         <div class="title-right">
    #             <h2 style="color:#22543d;margin-bottom:0;">Green Energy Plastic Tracker</h2>
    #             <p style="color:#22543d;font-weight:bold;">Powered by Acies Global</p>
    #         </div>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
