import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from datetime import date

about_page = st.Page(
    page="about.py",
    title="About me",
    #   icon=":material/thump_up:",
    default=True,
)

project_1_page = st.Page(
    page="Quotation.py",
    title="Quotation",
    #  icon=":material/bar_chart:",
)


project_2_page = st.Page(
    page="Samples.py",
    title="Samples",
    #  icon=":material/smart_toy:",
)


# --- Navigation Setup ----

#pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page]
    }
)


# --- Run information ----

pg.run()

