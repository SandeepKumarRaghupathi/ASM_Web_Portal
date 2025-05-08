import os
import streamlit as st
import pandas as pd
from datetime import date
import gspread
from google.oauth2 import service_account

# Define scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
creds_dict = st.secrets["gcp_service_account"]
creds = service_account.Credentials.from_service_account_info(
    creds_dict, scopes=SCOPES
)

client = gspread.authorize(creds)
# st.write("gcp_service_account" in st.secrets)  # Should print True

# Google Sheet details
SPREADSHEET_NAME = 'ASM Form'
SHEET_NAME_1 = 'Demand'
SHEET_NAME_2 = 'Quotation'

# Connect to Google Sheets
def connect_to_gsheet(creds, spreadsheet_name, sheet_name):
    client = gspread.authorize(creds)
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet.worksheet(sheet_name)

# Connect to sheets
sheet_by_name_2 = connect_to_gsheet(creds, SPREADSHEET_NAME, SHEET_NAME_2)
sheet_by_name_1 = connect_to_gsheet(creds, SPREADSHEET_NAME, SHEET_NAME_1)

# UI
st.title("Quotation")

# Read data from Google Sheets
def read_data():
    data = sheet_by_name_2.get_all_records()
    return pd.DataFrame(data)

st.table(read_data())

# Append new row
def add_data(row):
    sheet_by_name_1.append_row(row)

# List of material types
MATERIAL_TYPES = [
    "P-Sand", "M-Sand", "20MM", "12MM", "Chips-6MM", "Dust"
]

Orderdate = date.today()
today = date.today()

# Form UI
with st.expander("Place the Order"):
    with st.form(key="Quotation_form", clear_on_submit=True):
        Orderdate_str = Orderdate.strftime("%d-%m-%Y")
        First_Name = st.text_input(label="First_Name*")
        Mobile_Number = st.text_input(label="MobileNo*")
        Material_type = st.selectbox("MaterialType*", options=MATERIAL_TYPES, index=None)
        No_Units = st.slider("Units*", 0, 50, 1)
        Full_Address = st.text_input(label="FullAddress*")
        Delivery_Date = st.date_input(label="DeliveryDate", value=today, min_value=today)
        Delivery_Date_str = Delivery_Date.strftime("%d-%m-%Y")
        additional_info = st.text_area(label="Additional Notes")

        st.markdown("**Mandatory Fields*")
        submit_button = st.form_submit_button(label="Submit the Details")

        if submit_button:
            if not First_Name or not Mobile_Number or not Material_type or not No_Units or not Full_Address:
                st.warning("Ensure all mandatory fields are filled.")
                st.stop()
            elif not Mobile_Number.isdigit():
                st.error("Please enter mobile no in digits only.")
            elif len(Mobile_Number) != 10:
                st.warning("Mobile number should be 10 digits.")
            else:
                add_data([
                    Orderdate_str, First_Name, Mobile_Number, Material_type,
                    No_Units, Full_Address, Delivery_Date_str, additional_info
                ])
                st.success("Order Successfully Placed to ASM Company. We will get back to you shortly.")
