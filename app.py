import streamlit as st
import pandas as pd
import os

st.title("Faculty Course Preference Collection")

# Load course baskets
basket1 = pd.read_excel("courses.xlsx", sheet_name="Sheet1")
basket2 = pd.read_excel("courses.xlsx", sheet_name="Sheet2")

b1 = basket1.iloc[:,0].tolist()
b2 = basket2.iloc[:,0].tolist()

# Load employee file
employees = pd.read_excel("employees.xlsx")
employees.columns = employees.columns.str.strip()

empid = st.text_input("Enter Employee ID")

name=""
designation=""

if empid!="":

    emp = employees[employees["EmpID"].astype(str)==empid]

    if not emp.empty:

        name = emp.iloc[0]["Name"]
        designation = emp.iloc[0]["Designation"]

        st.success("Employee Found")
        st.write("Name:",name)
        st.write("Designation:",designation)

    else:
        st.error("Invalid Employee ID")

# ---------------- Basket 1 ----------------

st.header("Basket 1 Preferences")

basket1_pref=[]
available1=b1.copy()

for i in range(7):

    choice=st.selectbox(
        f"Preference {i+1}",
        available1,
        key=f"b1{i}"
    )

    basket1_pref.append(choice)

    if choice in available1:
        available1.remove(choice)

# ---------------- Basket 2 ----------------

st.header("Basket 2 Preferences")

basket2_pref=[]
available2=b2.copy()

for i in range(7):

    choice=st.selectbox(
        f"Preference {i+1}",
        available2,
        key=f"b2{i}"
    )

    basket2_pref.append(choice)

    if choice in available2:
        available2.remove(choice)

# ---------------- Submit ----------------

if st.button("Submit Preferences"):

    if empid=="" or name=="":
        st.error("Enter valid Employee ID")

    else:

        data={
        "EmpID":empid,
        "Name":name,
        "Designation":designation,
        "B1_P1":basket1_pref[0],
        "B1_P2":basket1_pref[1],
        "B1_P3":basket1_pref[2],
        "B1_P4":basket1_pref[3],
        "B1_P5":basket1_pref[4],
        "B1_P6":basket1_pref[5],
        "B1_P7":basket1_pref[6],
        "B2_P1":basket2_pref[0],
        "B2_P2":basket2_pref[1],
        "B2_P3":basket2_pref[2],
        "B2_P4":basket2_pref[3],
        "B2_P5":basket2_pref[4],
        "B2_P6":basket2_pref[5],
        "B2_P7":basket2_pref[6]
        }

        df=pd.DataFrame([data])

        file="responses.csv"

        if os.path.exists(file):

            old=pd.read_csv(file)

            if empid in old["EmpID"].astype(str).values:
                st.error("You already submitted preferences")
                st.stop()

            df=pd.concat([old,df],ignore_index=True)

        df.to_csv(file,index=False)

        st.success("Preferences submitted successfully")
