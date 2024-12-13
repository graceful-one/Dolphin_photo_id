import streamlit as st
import pandas as pd

dolphin_df = pd.read_csv(r"data/tblDolphin.csv", encoding="ISO-8859-1") #convert data into a dataframe
st.title("Dolphin Sightings Viewer") #streamlit title

#%% A try on making User text input
#Keyword search for dolphin name or fin shape
keyword = st.text_input("Search by Dolphin Name or Fin Shape (e.g., 'Cookie'🍪, 'Christmas'🎄, 'Garlic'🧄):")

#Prepare unique Dolphin IDs from the dataframe
dolphin_ids = dolphin_df['Dolphin_ID_Number'].unique()

#If a keyword is provided, filter the dolphins
if keyword:
    filtered_dolphins = dolphin_df[dolphin_df['Name'].str.contains(keyword, case=False, na=False) |
                                   dolphin_df['Fin_Shape_Family'].str.contains(keyword, case=False, na=False)]

    if len(filtered_dolphins) > 0:
        dolphin_ids_key = filtered_dolphins['Dolphin_ID_Number'].unique()
        selected_id = st.selectbox("Keywords Dolphin ID:", ["Select an option..."] + list(dolphin_ids_key), key="selectbox1")
    else:
        st.write("No dolphins found matching the keyword.")
else:
    #If no keyword is provided, just use the dropdown for selection
    selected_id = st.selectbox("Select Dolphin ID:", ["Select an option..."] + list(dolphin_ids))

filtered_data = df["Dolphin_ID_Number"] == selected_id #filter sightings for dolphin

if st.button("Show Dolphin Details"):
    if selected_id != "Select an option...":
        st.subheader(f"Sightings for {selected_id}:") #display results
        if not filtered_data.empty:
            for _, row in filtered_data.iterrows():
                st.write(f"Location: {row['Location']}, Date: {row['Date']}")
        else:
            st.write("No sightings found for this dolphin.")



location_file_path = './data/tblLocation.csv' 
location_data = pd.read_csv(location_file_path) #read csv
location_data.head() #read header
