#%% Prepare Packages  
import pandas as pd
import streamlit as st

#%% Get Data In
try:
    dolphin_df = pd.read_csv(r"tblDolphin.csv", encoding="ISO-8859-1")
    observations_df = pd.read_csv(r"tblDolphinsObserved.csv", encoding="ISO-8859-1")
except UnicodeDecodeError:
    st.error("There was an error reading the file due to encoding issues.")
except FileNotFoundError:
    st.error("The file was not found at the specified path.")

dolphin_df.head()

#%% Title of Application
st.title("Dolphin Query App")
st.markdown("### Select a Dolphin ID and Observation Date to view details.")

#%% A try on making User text input
#Keyword search for dolphin name or fin shape
keyword = st.text_input("Search by Dolphin Name or Fin Shape (e.g., 'Cookie' or 'Christmas'):")

# Filter dolphins based on the search keyword
if keyword:
    filtered_dolphins = dolphin_df[dolphin_df['Name'].str.contains(keyword, case=False, na=False) |
                                   dolphin_df['Fin_Shape_Family'].str.contains(keyword, case=False, na=False)]
    
    if len(filtered_dolphins) > 0:
        dolphin_ids_key = filtered_dolphins['Dolphin_ID_Number'].unique()
        selected_id = st.selectbox("Keywords Dolphin ID:", ["Select an option..."] + list(dolphin_ids_key), key="selectbox1")
    else:
        st.write("No dolphins found matching the keyword.")

#%%
# Prepare unique values
dolphin_ids = dolphin_df['Dolphin_ID_Number'].unique()
selected_id_two = st.selectbox("Select Dolphin ID:", ["Select an option..."] + list(dolphin_ids))

#%% Dolphin information that quried out
if st.button("Show Dolphin Details"):
     # Determine which Dolphin ID was selected
    if selected_id != "Select an option...":
        dolphin_id = selected_id
    elif selected_id_two != "Select an option...":
        dolphin_id = selected_id_two
    else:
        st.error("Please select a valid Dolphin ID.")
        dolphin_id = None  # Ensure no further processing occurs
    
    if dolphin_id:  # Proceed only if a valid dolphin_id exists
        result = dolphin_df[dolphin_df['Dolphin_ID_Number'] == dolphin_id]
        
        if not result.empty:
            st.write(f"### Information for Dolphin ID: {dolphin_id}")

            #%% Display Name if it exists
            dolphin_name = result.iloc[0]['Name']
            if pd.notna(dolphin_name):  # Check if the name exists (not NaN)
                st.write(f"**Dolphin Name:** {dolphin_name}")

            #%% Display Fin Shape, and Fin Shape Family if it exists
            st.write(f"**Fin Shape:** {result.iloc[0]['Fin']}")

            fin_shape_family = result.iloc[0]['Fin_Shape_Family']
            if pd.notna(fin_shape_family):  # Check if the Fin Shape Family exists (not NaN)
                st.write(f"**Fin Shape Family:** {fin_shape_family}")

            #%% Display DEAD status: If Dead is False, display alive message, else highlight "DEAD" in red
            if result.iloc[0]['Dead'] == False:
                st.write("**Dolphin is still alive**")
            else:
                st.markdown("<span style='color:red;'>**DEAD**</span>", unsafe_allow_html=True)

            #%% Display Gender information: Check if known female
            if result.iloc[0]['Known_Female'] == True:
                st.write("**She is a known female dolphin**")
            else:
                st.write("**Gender neutral**")

            #%% Display Comments if any content exists
            dolphin_comments = result.iloc[0]['Comments']
            if pd.notna(dolphin_comments) and dolphin_comments != '':
                st.write(f"**Comments:** {dolphin_comments}")

            #%% A Large Section of Displaying Date of Observations, with a plot showing frequency of sighting

            obs_dates = observations_df[observations_df['Dolphin ID Number'] == dolphin_id]['Trip Date'].unique()
            obs_dates = pd.to_datetime(obs_dates, errors='coerce')  # Convert to datetime

            #Sort dates in ascending order
            obs_dates = obs_dates.dropna().sort_values()

            st.write("### Observed on:")

            #Prepare sight numbers for plotting
            sight_numbers = observations_df[observations_df['Dolphin ID Number'] == dolphin_id]
            sight_numbers = sight_numbers[['Trip Date', 'Sight #']]

            # Convert 'Trip Date' to datetime and sort the data
            sight_numbers['Trip Date'] = pd.to_datetime(sight_numbers['Trip Date'], errors='coerce')
            sight_numbers = sight_numbers.dropna().sort_values('Trip Date')
            sight_numbers = sight_numbers.groupby('Trip Date')['Sight #'].sum().reset_index()

            # Plot using Streamlit's line_chart
            if not sight_numbers.empty:
                st.line_chart(
                    data=sight_numbers.set_index('Trip Date'),
                    y='Sight #',
                    use_container_width=True
                )
            else:
                st.write("No sightings data available for the selected Dolphin ID.")

            #Generate table of observation date
            if len(obs_dates) > 0:
                formatted_dates = obs_dates.strftime('%Y-%m-%d')
                dates_df = pd.DataFrame(formatted_dates, columns=["Date (Y/M/D)"])
                dates_df.index = ['First Observation'] + [str(i) for i in range(2, len(dates_df) + 1)]

                st.table(dates_df)
            
            else:
                st.write("No subsequent observation dates found.")

        else:
            st.error("No data available for the selected criteria.")
    else:
        st.error("Please select both Dolphin ID and Observation Date.")

# %%
