#%% Prepare Packages  
import pandas as pd
import streamlit as st
import pip
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
install("dropbox")
import dropbox
from PIL import Image
import numpy as np
import io
import requests

#%% Get Data In
try:
    dolphin_df = pd.read_csv(r"tblDolphin.csv", encoding="ISO-8859-1")
    observations_df = pd.read_csv(r"tblDolphinsObserved.csv", encoding="ISO-8859-1")
except UnicodeDecodeError:
    st.error("There was an error reading the file due to encoding issues.")
except FileNotFoundError:
    st.error("The file was not found at the specified path.")

dolphin_df.head()

###%% Get Photo In
#%% Dropbox Configuration
# Replace with your refresh token, client ID, and client secret
REFRESH_TOKEN = 'f_IpZCDhQnkAAAAAAAAAAWCYKK8_vIqF3vPey5UuOfwFsvvnaSmn1bucmtrH4ntx'
CLIENT_ID = 'y0bkdjd40l2ck3o'
CLIENT_SECRET = '95pjufdudglbg8s'

def refresh_access_token(refresh_token):
    """Use the refresh token to get a new access token."""
    url = 'https://api.dropbox.com/oauth2/token'
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data['access_token']
    else:
        st.error("Error refreshing Dropbox token.")
        return None

ACCESS_TOKEN = refresh_access_token(REFRESH_TOKEN)
if ACCESS_TOKEN:
    dbx = dropbox.Dropbox(ACCESS_TOKEN)


def get_file_from_dropbox(path):
    """Fetch a file from Dropbox and return it as a NumPy array."""
    try:
        _, res = dbx.files_download(path)
        file_buffer = io.BytesIO(res.content)
        image = Image.open(file_buffer)
        return np.array(image)
    except dropbox.exceptions.ApiError:
        return None


def get_photo(dolphin_id, side):
    """Retrieve and display a dolphin photo."""
    try:
        file_path = f'/BestOfPhotos/{dolphin_id}{side}.jpg'
        image_object = get_file_from_dropbox(file_path)
        if image_object is None:
            file_path = '/BestOfPhotos/no_photo.jpg'
            image_object = get_file_from_dropbox(file_path)
        return image_object
    except Exception as e:
        st.error(f"Failed to retrieve image for Dolphin {dolphin_id} ({side}): {e}")
        return None

#%% Title of Application
st.title("Find a Dolphin🐬")
st.markdown("### Select a dolphin ID or keywords about dolphin to find more details")

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

#%% Dolphin information that quried out
if st.button("Show Dolphin Details"):
    if selected_id != "Select an option...":
        result = dolphin_df[(dolphin_df['Dolphin_ID_Number'] == selected_id)]
        
        if not result.empty:
            st.write(f"### Information for Dolphin ID: {selected_id}")

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
                st.write("**Life Condition: Dolphin is still alive**")
            else:
                st.markdown("<span style='color:red;'>**DEAD**</span>", unsafe_allow_html=True)

            #%% Display Gender information: Check if known female
            if result.iloc[0]['Known_Female'] == True:
                st.write("**Gender: She is a known female dolphin**")
            else:
                st.write("**Gender: Not Confirmed**")

            #%% Display Comments if any content exists
            dolphin_comments = result.iloc[0]['Comments']
            if pd.notna(dolphin_comments) and dolphin_comments != '':
                st.write(f"**Comments:** {dolphin_comments}")
            
            #%% Display Photo Section
            st.write("### Photo of Fin:")

            # Create two columns for the left and right photos
            col1, col2 = st.columns(2)

            # Retrieve and display the left side photo
            with col1:
                left_image = get_photo(selected_id, "L")
                if left_image is not None:
                    st.image(left_image, caption=f"Dolphin {selected_id} (Left Side)", use_container_width=True)
                else:
                    st.write("No photo available for the left side.")

            # Retrieve and display the right side photo
            with col2:
                right_image = get_photo(selected_id, "R")
                if right_image is not None:
                    st.image(right_image, caption=f"Dolphin {selected_id} (Right Side)", use_container_width=True)
                else:
                    st.write("No photo available for the right side.")

            #%% A Large Section of Displaying Date of Observations, with a plot showing frequency of sighting

            obs_dates = observations_df[observations_df['Dolphin ID Number'] == selected_id]['Trip Date'].unique()
            obs_dates = pd.to_datetime(obs_dates, errors='coerce')  # Convert to datetime

            #Sort dates in ascending order
            obs_dates = obs_dates.dropna().sort_values()

            st.write("### Observed on:")

            #Prepare sight numbers for plotting
            sight_numbers = observations_df[observations_df['Dolphin ID Number'] == selected_id]
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
                    y_label = "Count of Sighting",
                    color = "#1134A6",
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
