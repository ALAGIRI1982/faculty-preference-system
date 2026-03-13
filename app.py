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
# Response File
# -----------------------------

file = "responses.csv"

header = [
"EmpID","Name","Designation",
"B1_P1","B1_P2","B1_P3","B1_P4","B1_P5","B1_P6","B1_P7",
"B2_P1","B2_P2","B2_P3","B2_P4","B2_P5","B2_P6","B2_P7"
]

# -----------------------------
# Save Response Function
# -----------------------------

def save_response(row):

    file_exists = os.path.isfile(file)

    with open(file,"a",newline="") as f:

        writer = csv.writer(f)

        if not file_exists or os.stat(file).st_size == 0:
            writer.writerow(header)

        writer.writerow(row)

# -----------------------------
# UI
# -----------------------------

st.title("Faculty Course Preference System")

empid = st.text_input("Enter Employee ID")

name=""
designation=""

if empid:

    emp = employees[employees["EmpID"].astype(str)==empid]

    if not emp.empty:

        name = emp.iloc[0]["Name"]
        designation = emp.iloc[0]["Designation"]

        st.write("Name :",name)
        st.write("Designation :",designation)

    else:

        st.error("Employee ID not found")

# -----------------------------
# Basket 1 Preferences
# -----------------------------

st.subheader("Basket 1 Preferences")

basket1_pref=[]
available1=basket1.copy()

for i in range(7):

    pref = st.selectbox(
        f"Basket1 Preference {i+1}",
        [""]+available1,
        key=f"b1_{i}"
    )

    basket1_pref.append(pref)

    if pref in available1:
        available1.remove(pref)

# -----------------------------
# Basket 2 Preferences
# -----------------------------

st.subheader("Basket 2 Preferences")

basket2_pref=[]
available2=basket2.copy()

for i in range(7):

    pref = st.selectbox(
        f"Basket2 Preference {i+1}",
        [""]+available2,
        key=f"b2_{i}"
    )

    basket2_pref.append(pref)

    if pref in available2:
        available2.remove(pref)

# -----------------------------
# Submit Button
# -----------------------------

if st.button("Submit Preferences"):

    b1=[x for x in basket1_pref if x!=""]
    b2=[x for x in basket2_pref if x!=""]

    if len(set(b1))!=len(b1):
        st.error("Duplicate course in Basket 1")

    elif len(set(b2))!=len(b2):
        st.error("Duplicate course in Basket 2")

    else:

        row=[
        empid,
        name,
        designation,
        *basket1_pref,
        *basket2_pref
        ]

        save_response(row)

        st.success("Preferences submitted successfully")
