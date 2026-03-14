import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.title("Faculty Course Preference System")

# -----------------------------
# Load Courses from Excel
# -----------------------------

courses = pd.read_excel("courses.xlsx")

basket1 = courses["Basket1"].dropna().tolist()
basket2 = courses["Basket2"].dropna().tolist()


# -----------------------------
# Google Sheet Connection
# -----------------------------

scope = [
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
st.secrets["gcp_service_account"],
scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key("YOUR_SHEET_ID").sheet1


# -----------------------------
# Create Header Automatically
# -----------------------------

header = ["Timestamp","Faculty_Name","Faculty_ID","Basket1","Basket2"]

if sheet.row_values(1) != header:
    sheet.insert_row(header,1)


# -----------------------------
# Faculty Information
# -----------------------------

faculty_name = st.text_input("Faculty Name")
faculty_id = st.text_input("Faculty ID / Email")


# -----------------------------
# Basket Selection
# -----------------------------

st.subheader("Basket 1 Course Selection")
pref1 = st.multiselect("Select Courses", basket1)

st.subheader("Basket 2 Course Selection")
pref2 = st.multiselect("Select Courses ", basket2)


# -----------------------------
# Submit Button
# -----------------------------

if st.button("Submit Preference"):

    if faculty_name == "" or faculty_id == "":
        st.error("Enter faculty details")

    else:

        data = sheet.get_all_records()

        existing_ids = [row["Faculty_ID"] for row in data]

        if faculty_id in existing_ids:
            st.error("You already submitted preference")

        else:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sheet.append_row([
                timestamp,
                faculty_name,
                faculty_id,
                ", ".join(pref1),
                ", ".join(pref2)
            ])

            st.success("Preference submitted successfully")
