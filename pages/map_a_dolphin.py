import streamlit as st
import pandas as pd

df=pd.read_csv(r"data/tblDolphin.csv", encoding="ISO-8859-1") #convert data into a dataframe
st.title("Dolphin Sightings Viewer") #streamlit title

dolphins = df["Dolphin_Name"].unique() #streamlit dropdown 
selected_dolphin = st.selectbox("Select a Dolphin:", options=dolphins)

filtered_data = df[df["Dolphin_Name"] == selected_dolphin] #filter sightings for dolphin

st.subheader(f"Sightings for {selected_dolphin}:") #display results
if not filtered_data.empty:
    for _, row in filtered_data.iterrows():
        st.write(f"Location: {row['Location']}, Date: {row['Date']}")
else:
    st.write("No sightings found for this dolphin.")

location_file_path = './data/tblLocation.csv' 
location_data = pd.read_csv(location_file_path) #read csv
location_data.head() #read header
