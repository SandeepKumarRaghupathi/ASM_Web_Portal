import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import streamlit as st
import pandas as pd
from datetime import date
import os

# # Confirm env var is available
# if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
#     raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set.")

# # Load credentials from env var path
# CREDENTIALS_FILE = service_account.Credentials.from_service_account_file(
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
#     scopes=["https://www.googleapis.com/auth/spreadsheets"]
# )

# # # Load credentials from environment
# # CREDENTIALS_FILE = service_account.Credentials.from_service_account_file(
# #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
# #     scopes=["https://www.googleapis.com/auth/spreadsheets"]
# # )
# print("GOOGLE_APPLICATION_CREDENTIALS" in os.environ)  # Should print True

# CREDENTIALS_FILE = service_account.Credentials.from_service_account_file(
#     "$PWD/gcp-key.json",  # hardcoded path
#     scopes=["https://www.googleapis.com/auth/spreadsheets"]
# )

Authenticate and connect to Google Sheets
def connect_to_gsheet(creds_json, spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet.worksheet(sheet_name)  # Access specific sheet by name


# Google Sheet credentials and details
SPREADSHEET_NAME = 'ASM Form'
SHEET_NAME_1 = 'Demand'
SHEET_NAME_2 = 'Quotation'
# CREDENTIALS_FILE = 'asm-web-portal-66eaab8ed9f6.json'

Connect to the Google Sheet
sheet_by_name_2 = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, sheet_name=SHEET_NAME_2)
sheet_by_name_1 = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, sheet_name=SHEET_NAME_1)


st.title("Quotation")

# Read Data from Google Sheets
def read_data():
    data = sheet_by_name_2.get_all_records()  # Get all records from Google Sheet
    return pd.DataFrame(data)

st.table(read_data())

# Append the row to the Google Sheet
def add_data(row):
    sheet_by_name_1.append_row(row)

# # Initialize session state variables only once
# if "reset" not in st.session_state:
#     st.session_state.reset = False
# def clear_form():
#     st.session_state["First_Name"] = ""
#     st.session_state["Mobile_Number"] = ""
#     st.session_state["Material_type"] = ""
#     st.session_state["No_Units"] = 0
#     st.session_state["Full_Address"] = ""
#     st.session_state["Delivery_Date"] = date.today()
#     st.session_state["additional_info"] = ""
#     st.session_state["reset"] = True

# List of Business Types and Products
MATERIAL_TYPES = [
    "P-Sand",
    "M-Sand",
    "Chips-20MM",
    "Gravel",
]

# # Store default (frozen) date
# if "Orderdate" not in st.session_state:
#     st.session_state.Orderdate = date.today()

Orderdate = date.today()
today = date.today()

# Onboarding New Vendor Form
with st.expander("Place the Order"):
    with st.form(key="Quotation_form", clear_on_submit=True):
        # Orderdate = st.date_input(label="Ordeplaced_Date", value=Orderdate)
        Orderdate = Orderdate.strftime("%d-%m-%Y")
        First_Name = st.text_input(label="First_Name*")
        Mobile_Number = st.text_input(label="MobileNo*")
        Material_type = st.selectbox("MaterialType*", options=MATERIAL_TYPES, index=None)
        No_Units = st.slider("Units*", 0, 50, 1)
        Full_Address = st.text_input(label="FullAddress*")
        Delivery_Date = st.date_input(label="DeliveryDate", value=today, min_value=today)
        Delivery_Date = Delivery_Date.strftime("%d-%m-%Y")
        additional_info = st.text_area(label="Additional Notes")

        # Mark mandatory fields
        st.markdown("**Mandatory Fields*")

        # Submit button inside the form
        submit_button = st.form_submit_button(label="Submit the Details")
        # Clear_Button = st.form_submit_button(label="Clear")

        # If the submit button is pressed
        if submit_button:
            # Check if all mandatory fields are filled
            if not First_Name or not Mobile_Number or not Material_type or not No_Units or not Full_Address:
                st.warning("Ensure all mandatory fields are filled.")
                st.stop()
            elif Mobile_Number and not Mobile_Number.isdigit():
                    st.error("Please enter mobile no in digits only.")
            elif Mobile_Number and len(Mobile_Number) != 10:
                    st.warning("Mobile number should be 10 digits.")
            else:
                # Orderdate = st.write("Orderplaced_Date", Orderdate)
                add_data([Orderdate, First_Name, Mobile_Number, Material_type, No_Units, Full_Address, Delivery_Date, additional_info])  # Append the row to the sheet
                st.success("Order Successfully Placed to ASM Company. We will get back to you shortly")

    # if st.form_submit_button("Clear"):
    #     clear_form()







            # def existing_data():
            #     data_2 = sheet_by_name_1.get_all_records()  # Get all records from Google Sheet
            #     return pd.DataFrame(data_2)
            #
            # st.table(existing_data())
            # print(type(existing_data))

            # @st.dialog("Fill the form for delivery")
            # def show_contact_form():
            #     st.text_input("First Name")
            #     st.text_input("Last Name")
            #     st.text_input("Mobile No")
            #     st.text_input("Address")
            #     st.text_input("Delivery Date")
            #     if st.button("Submit"):
            #         st.success("Delivery Details Submitted")
            #
            # if st.button("Delivery Details", key="green"):
            #     show_contact_form()

            # Fetch existing vendors data
            # existing_data = connect_to_gsheet.read(worksheet="Demand", usecols=list(range(6)), ttl=5)
            # existing_data = existing_data.dropna(how="all")


            # Create a new row of vendor data
            # vendor_data = pd.DataFrame(
            #     [
            #         {
            #             st.write("First_Name", First_Name),
            #             st.write("MobileNo", Mobile_Number),
            #             st.write("MaterialType", Material_type),
            #             st.write("Units", No_Units),
            #             st.write("FullAddress", Full_Address),
            #             st.write("DeliveryDate", Delivery_Date.strftime("%d-%m-%Y")),
            #             st.write("Additional Info", additional_info),
            #         }
            #     ]
            # )
            # print(type(vendor_data))

            # def vendor_details ():
            #     data_3 = vendor_data
            # print(type(vendor_details()))
            # Add the new vendor data to the existing data
            # updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # # Update Google Sheets with the new vendor data
            # conn.update(worksheet="Vendors", data=updated_df)

            # combined_data = pd.concat([existing_data(), vendor_data()], ignore_index=True)
            #
            # # Display the combined data
            # # st.dataframe(combined_data)
            # print(type(combined_data))
            #
            # st.success("Successfully submitted!")

# gsheet = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, sheet_name=SHEET_NAME_2)  # Call the function
#             # Update Google Sheets with the new vendor data
#             # worksheet = gsheet.worksheet("vendor_data")
#             # worksheet.update([updated_df.columns.values.tolist()] + updated_df.values.tolist())
#             # # gsheet.update(worksheet="vendor_data", data=updated_df)
#             # Correct approach
#             gc = gspread.service_account(filename="/Users/sandeepkumar/PycharmProjects/.streamlit/credentials.json")
#             spreadsheet = gc.open("ASM Form")
#             worksheet = spreadsheet.worksheet("Demand")
#             updated_df = pd.concat([vendor_data], ignore_index=True)
#
# import streamlit as st
# from streamlit import GSheetsClient
# import pandas as pd
#
# # Display Title
# st.title("Quotation")
#
#
# # Establishing a Google Sheets connection
# conn = st.connection("gsheets", type="gspread", secrets="secrets.toml")
#
# # Fetch existing vendor data
# existing_data = conn.read(worksheet="Quotation", usecols=list(range(6)),ttl=5)
# existing_data = existing_data.dropna(how="all")
#
# st.dataframe(existing_data)
#
# data = {
#     "Name": ["P-Sand", "M-Sand", "Chips 20mm"],
#     "Unit": [1, 1, 1],
#     "Price": ["8000", "6000", "5000"]
# }
#
# # Convert to DataFrame
# df = pd.DataFrame(data)
#
# # Display as static table
# st.write("### Material Details")
# st.table(df)
#
# # Google Sheets setup
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/sandeepkumar/PycharmProjects/Web Dev/your_credentials.json', scope)
# client = gspread.authorize(credentials)
#
#
# @st.dialog("Fill the form for delivery")
# def show_contact_form():
#     FirstName = st.text_input("First Name")
#     LastName = st.text_input("Last Name")
#     MobileNo = st.text_input("Mobile No")
#     Address = st.text_input("Address")
#     DeliveryDate = st.text_input("Delivery Date")
#     if st.button("Delivery Details"):
#         data = [First_Name, Last_Name, Mobile_No, Address, Delivery_Date]
#         # Append data to sheet
#         sheet.append_row(data)
#         st.success("Data successfully saved to Google Sheet!")
#         st.success("Delivery Details Submitted")
#         show_contact_form()
#
#
#
