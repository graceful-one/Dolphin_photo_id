# install packages
import os 
import streamlit as st
import datetime
import pandas as pd
from openpyxl import load_workbook
import uuid

#load existing dolphin observation dataset
file_path = './tblDolphin.xlsx'

#load excel file
try:
    existing_data = pd.read_excel(excel_file) #from pandas, used to read file
except Exception as e: #from python to handle errors
    st.error(f"Error loading the Excel file: {e}") #function from streamlit for errors
    existing_data = None #if file is missing or invalid, program does not crash

#set up streamlit app
st.title("Dolphin Observation Data Entry)
st.write("Add new observation data to the database.")

#create a form 
with st.form(key="data_entry_form"):
  st.subheader("Enter Observation Details") #ask user questions
  #autonum
  #trip_date = st.date_input(format="YYYY/MM/DD") #https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
  #trip_time = st.time_input() #https://docs.streamlit.io/develop/api-reference/widgets/st.time_input
  trip_num = st.text_input("Trip #) #https://docs.streamlit.io/develop/api-reference/widgets/st.time_input
  sight_num = st.number_input("Sight #") #https://docs.streamlit.io/develop/api-reference/widgets/st.number_input
  dolphin_id_num = st.number_input("Dolphin ID Number")
  new_dolphin = st.checkbox("New Dolphin?") #https://docs.streamlit.io/develop/api-reference/widgets/st.checkbox
  resight = st.checkbox("Resight?")
  seen_offshore = st.checkbox("Seen Offshore?")
  #s_GUID
  clarity = st.number_input("Clarity")
  contrast = st.number_input("Contrast")
  angle = st.number_input("Angle")
  partial = st.checkbox("Partial")
  overall = st.number_input("Overall")
  distinctiveness = st.number_input("Distinctiveness")
  verified = st.checkbox("Verified")

