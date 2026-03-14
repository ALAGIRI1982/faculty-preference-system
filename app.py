import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.title("Faculty Course Preference System")

# -----------------------
# Load Employee Data
# -----------------------

emp_data = pd.read_excel("employees.xlsx", engine="openpyxl")

# -----------------------
# Load Course Data
# -----------------------

basket1_df = pd.read_excel("courses.xlsx", sheet_name="Sheet1", engine="openpyxl")
basket2_df = pd.read_excel("courses.xlsx", sheet_name="Sheet2", engine="openpyxl")

basket1 = basket1_df.iloc[:,0].dropna().tolist()
basket2 = basket2_df.iloc[:,0].dropna().tolist()

# -----------------------
# Google Sheet Connection
# -----------------------

scope = [
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
st.secrets["gcp_service_account"],
scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key("1y1a9UvWW-xrIBR7-hEWn70I7NmsSHpX3AEspg-PLXfg").sheet1

# -----------------------
# Auto Header Creation
# -----------------------

header = [
"Timestamp",
"EmpID",
"Name",
"Designation",
"Basket1",
"Basket2"
]

if sheet.row_values(1) != header:
    sheet.insert_row(header,1)

# -----------------------
# Employee ID Input
# -----------------------

emp_id = st.text_input("Enter Employee ID")

name = ""
designation = ""

if emp_id != "":

    emp = emp_data[emp_data["EmpID"].astype(str) == emp_id]

    if not emp.empty:

        name = emp.iloc[0]["Name"]
        designation = emp.iloc[0]["Designation"]

        st.success("Employee Found")

        st.write("Name :", name)
        st.write("Designation :", designation)

    else:

        st.error("Invalid Employee ID")

# -----------------------
# Basket Selection
# -----------------------

st.subheader("Basket 1 Courses (Select exactly 7)")

pref1 = st.multiselect(
"Basket1",
basket1,
max_selections=7
)

st.subheader("Basket 2 Courses (Select exactly 7)")

pref2 = st.multiselect(
"Basket2",
basket2,
max_selections=7
)

# -----------------------
# Submit
# -----------------------

if st.button("Submit Preference"):

    if emp_id == "" or name == "":
        st.error("Enter valid Employee ID")

    elif len(pref1) != 7 or len(pref2) != 7:
        st.error("Select exactly 7 courses in each basket")

    else:

        data = sheet.get_all_records()

        existing_ids = [str(row["EmpID"]) for row in data]

        if emp_id in existing_ids:

            st.error("You already submitted preference")

        else:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sheet.append_row([
                timestamp,
                emp_id,
                name,
                designation,
                ", ".join(pref1),
                ", ".join(pref2)
            ])

            st.success("Preference Submitted Successfully")
