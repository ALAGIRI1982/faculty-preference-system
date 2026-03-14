import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("Faculty Course Preference System")

# -----------------------------
# GOOGLE SHEETS CONNECTION
# -----------------------------

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)

client = gspread.authorize(creds)

SHEET_ID = "1y1a9UvWW-xrIBR7-hEWn70I7NmsSHpX3AEspg-PLXfg"

sheet = client.open_by_key(SHEET_ID).sheet1


# -----------------------------
# CREATE HEADER AUTOMATICALLY
# -----------------------------

headers = [
    "EmpID",
    "Name",
    "Designation",
    "BS1P1","BS1P2","BS1P3","BS1P4","BS1P5","BS1P6","BS1P7",
    "BS2P1","BS2P2","BS2P3","BS2P4","BS2P5","BS2P6","BS2P7"
]

first_row = sheet.row_values(1)

if first_row != headers:
    sheet.update('A1:Q1', [headers])


# -----------------------------
# LOAD COURSE FILE
# -----------------------------

courses = pd.read_excel("courses.xlsx", sheet_name=None)

basket1 = courses["Sheet1"]["Course"].dropna().tolist()
basket2 = courses["Sheet2"]["Course"].dropna().tolist()


# -----------------------------
# LOAD EMPLOYEE FILE
# -----------------------------

employees = pd.read_excel("employees.xlsx")


# -----------------------------
# EMPLOYEE ID INPUT
# -----------------------------

emp_id = st.text_input("Enter Employee ID")

name = ""
designation = ""

if emp_id:

    emp_row = employees[employees["EmpID"].astype(str) == emp_id]

    if not emp_row.empty:

        name = emp_row.iloc[0]["Name"]
        designation = emp_row.iloc[0]["Designation"]

        st.success("Employee Found")

        st.write("Name:", name)
        st.write("Designation:", designation)

    else:

        st.error("Invalid Employee ID")


# -----------------------------
# PREVENT DUPLICATE SUBMISSION
# -----------------------------

existing_ids = sheet.col_values(1)

if emp_id and emp_id in existing_ids:
    st.warning("You have already submitted your preferences")
    st.stop()


# -----------------------------
# BASKET 1 PREFERENCES
# -----------------------------

if name != "":

    st.subheader("Basket 1 Preferences")

    basket1_pref = []

    for i in range(1,8):

        course = st.selectbox(
            f"BS1P{i}",
            basket1,
            key=f"b1{i}"
        )

        basket1_pref.append(course)


# -----------------------------
# BASKET 2 PREFERENCES
# -----------------------------

    st.subheader("Basket 2 Preferences")

    basket2_pref = []

    for i in range(1,8):

        course = st.selectbox(
            f"BS2P{i}",
            basket2,
            key=f"b2{i}"
        )

        basket2_pref.append(course)


# -----------------------------
# SUBMIT BUTTON
# -----------------------------

    if st.button("Submit Preference"):

        if len(set(basket1_pref)) != 7:
            st.error("Basket1 preferences must be unique")
            st.stop()

        if len(set(basket2_pref)) != 7:
            st.error("Basket2 preferences must be unique")
            st.stop()

        row = [
            emp_id,
            name,
            designation,
            *basket1_pref,
            *basket2_pref
        ]

        sheet.append_row(row)

        st.success("Preference Submitted Successfully")
