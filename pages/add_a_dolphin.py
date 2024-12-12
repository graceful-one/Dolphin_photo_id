# install packages
import os 
import streamlit as st
import datetime
import pandas as pd
import uuid

#load existing dolphin observation dataset
file_path = './tblDolphin.csv'

#load excel file
if os.path.exists(file_path):
    existing_data = pd.read_csv(file_path) #from pandas, used to read file
else:
    exisiting_data = pd.DataFrame(columns=[
        "Trip #", "Sight #", "Dolphin ID Number", "New Dolphin?", "Resight?",
        "Seen Offshore?", "Clarity", "Contrast", "Angle", "Partial",
        "Overall", "Distinctiveness", "Verified"])

#set up streamlit app
st.title("Dolphin Observation Data Entry")
st.write("Add new observation data to the database.")

#create a form 
with st.form(key="data_entry_form"):{
  st.subheader("Enter Observation Details") #ask user questions
  #autonum
  #trip_date = st.date_input(format="YYYY/MM/DD") #https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
  #trip_time = st.time_input() #https://docs.streamlit.io/develop/api-reference/widgets/st.time_input
  trip_num = st.text_input("Trip #") #https://docs.streamlit.io/develop/api-reference/widgets/st.time_input
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
  }

st.form_submit_button()

if submitted:
    new_row = { #dictionary
        "Trip #": trip_num,
        "Sight #": sight_num,
        "Dolphin ID Number": dolphin_id_num,
        "New Dolphin?": new_dolphin,
        "Resight?": resight,
        "Seen Offshore?": seen_offshore,
        "Clarity": clarity,
        "Contrast": contrast,
        "Angle": angle,
        "Partial": partial,
        "Overall": overall,
        "Distinctiveness": distinctiveness,
        "Verified": verified,
    }

updated_data = existing_data.append(new_row, ignore_index=True) #append new row 

updated_data.to_csv(file_path, index=False) #save updates

st.success("Observation added!") #confirm data addition
