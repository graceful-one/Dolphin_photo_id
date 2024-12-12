import streamlit as st
import pandas as pd

#convert data into a dataframe
df = pd.DataFrame(tblDolphin.csv)

#streamlit title
st.title("Dolphin Sightings Viewer")

#streamlit dropdown 
dolphins = df["Dolphin_Name"].unique()
selected_dolphin = st.selectbox("Select a Dolphin:", options=dolphins)

#filter sightings for dolphin
filtered_data = df[df["Dolphin_Name"] == selected_dolphin]

#display results
st.subheader(f"Sightings for {selected_dolphin}:")
if not filtered_data.empty:
    for _, row in filtered_data.iterrows():
        st.write(f"Location: {row['Location']}, Date: {row['Date']}")
else:
    st.write("No sightings found for this dolphin.")
