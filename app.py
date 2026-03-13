import streamlit as st
import pandas as pd
import csv
import os

# -----------------------------
# Load Course Data
# -----------------------------
courses = pd.read_excel("courses.xlsx", sheet_name=None)

basket1 = courses["Sheet1"]["Course"].dropna().tolist()
basket2 = courses["Sheet2"]["Course"].dropna().tolist()

# -----------------------------
# Load Employee Data
# -----------------------------
employees = pd.read_excel("employees.xlsx")

# -----------------------------
# CSV Response File
# -----------------------------
file = "responses.csv"

header = [
    "EmpID", "Name", "Designation",
    "B1_P1","B1_P2","B1_P3","B1_P4","B1_P5","B1_P6","B1_P7",
    "B2_P1","B2_P2","B2_P3","B2_P4","B2_P5","B2_P6","B2_P7"
]

if not os.path.isfile(file) or os.stat(file).st_size == 0:
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

# -----------------------------
# Save Response Function
# -----------------------------
def save_response(row):
    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
        f.flush()

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
# Initialize Session State
# -----------------------------
if "basket1_pref" not in st.session_state:
    st.session_state.basket1_pref = [""] * 7

if "basket2_pref" not in st.session_state:
    st.session_state.basket2_pref = [""] * 7

# -----------------------------
# Basket 1 Selection
# -----------------------------
st.subheader("Basket 1 Preferences")
for i in range(7):
    # Include current value in available list to retain selection
    available1 = [c for c in basket1 if c not in st.session_state.basket1_pref or c == st.session_state.basket1_pref[i]]
    pref = st.selectbox(
        f"Basket1 Preference {i+1}",
        [""] + available1,
        key=f"b1_{i}",
        format_func=lambda x: x
    )
    st.session_state.basket1_pref[i] = pref

# -----------------------------
# Basket 2 Selection
# -----------------------------
st.subheader("Basket 2 Preferences")
for i in range(7):
    available2 = [c for c in basket2 if c not in st.session_state.basket2_pref or c == st.session_state.basket2_pref[i]]
    pref = st.selectbox(
        f"Basket2 Preference {i+1}",
        [""] + available2,
        key=f"b2_{i}",
        format_func=lambda x: x
    )
    st.session_state.basket2_pref[i] = pref

# -----------------------------
# Submit Button
# -----------------------------
if st.button("Submit Preferences"):
    b1 = [x for x in st.session_state.basket1_pref if x != ""]
    b2 = [x for x in st.session_state.basket2_pref if x != ""]

    if len(set(b1)) != len(b1):
        st.error("Duplicate course selected in Basket 1")
    elif len(set(b2)) != len(b2):
        st.error("Duplicate course selected in Basket 2")
    elif "" in b1 or "" in b2:
        st.error("Please select all 7 courses in both baskets")
    else:
        row = [empid, name, designation, *st.session_state.basket1_pref, *st.session_state.basket2_pref]
        save_response(row)
        st.success("Preferences submitted successfully!")

        # Clear session state after submission
        st.session_state.basket1_pref = [""] * 7
        st.session_state.basket2_pref = [""] * 7
