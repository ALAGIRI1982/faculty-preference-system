import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# Google Sheet Connection
# -----------------------------
scope = [
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
"service_account.json", scope)

client = gspread.authorize(creds)

sheet = client.open_by_key("PASTE_YOUR_SHEET_ID_HERE").sheet1

# -----------------------------
# Function to Check Duplicate EmpID
# -----------------------------
def empid_exists(empid):

    records = sheet.col_values(1)

    if empid in records:
        return True
    else:
        return False


# -----------------------------
# Load Employee Data
# -----------------------------
employees = pd.read_excel("employees.xlsx")

# -----------------------------
# Load Course Data
# -----------------------------
courses = pd.read_excel("courses.xlsx", sheet_name=None)

basket1 = courses["Sheet1"]["Course"].dropna().tolist()
basket2 = courses["Sheet2"]["Course"].dropna().tolist()

# -----------------------------
# Session State Initialization
# -----------------------------
if "basket1_pref" not in st.session_state:
    st.session_state.basket1_pref = [""] * 7

if "basket2_pref" not in st.session_state:
    st.session_state.basket2_pref = [""] * 7

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Faculty Course Preference System")

empid = st.text_input("Enter Employee ID")

name = ""
designation = ""

if empid:

    emp = employees[employees["EmpID"].astype(str) == empid]

    if not emp.empty:

        name = emp.iloc[0]["Name"]
        designation = emp.iloc[0]["Designation"]

        st.write("Name:", name)
        st.write("Designation:", designation)

    else:
        st.error("Employee ID not found")

# -----------------------------
# Basket 1 Preferences
# -----------------------------
st.subheader("Basket 1 Preferences")

for i in range(7):

    available = [c for c in basket1 if c not in st.session_state.basket1_pref]

    pref = st.selectbox(
        f"Basket1 Preference {i+1}",
        [""] + available,
        key=f"b1_{i}"
    )

    st.session_state.basket1_pref[i] = pref


# -----------------------------
# Basket 2 Preferences
# -----------------------------
st.subheader("Basket 2 Preferences")

for i in range(7):

    available = [c for c in basket2 if c not in st.session_state.basket2_pref]

    pref = st.selectbox(
        f"Basket2 Preference {i+1}",
        [""] + available,
        key=f"b2_{i}"
    )

    st.session_state.basket2_pref[i] = pref


# -----------------------------
# Submit Button
# -----------------------------
if st.button("Submit Preferences"):

    if empid == "":
        st.error("Please enter Employee ID")

    elif empid_exists(empid):
        st.error("You have already submitted your preferences")

    elif "" in st.session_state.basket1_pref:
        st.error("Select all 7 courses in Basket 1")

    elif "" in st.session_state.basket2_pref:
        st.error("Select all 7 courses in Basket 2")

    else:

        row = [
            empid,
            name,
            designation,
            *st.session_state.basket1_pref,
            *st.session_state.basket2_pref
        ]

        sheet.append_row(row)

        st.success("Preferences submitted successfully!")

        # Clear selections after submit
        st.session_state.basket1_pref = [""] * 7
        st.session_state.basket2_pref = [""] * 7
