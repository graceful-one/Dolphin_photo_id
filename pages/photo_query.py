

## install packages
import streamlit as st
import pandas as pd 
import io
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

st.title("Photo APP")

dolphin_id = st.text_input("Enter Dolphin ID (e.g., 0000a):")
side = st.radio("Select Fin Side:", ["R", "L"])
## install packages

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
install("dropbox")
import dropbox
from PIL import Image
import numpy as np
import requests
import dropbox

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

    # Make the POST request to get a new access token
    response = requests.post(url, data=payload)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        return data['access_token']  # Return the new access token
    else:
        print(f"Error refreshing token: {response.json()}")
        return None

# Example usage:
ACCESS_TOKEN = refresh_access_token(REFRESH_TOKEN)
if ACCESS_TOKEN:
    # Now you can use the new access token for Dropbox API calls
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    print("Access token refreshed and Dropbox client initialized.")


def get_file_from_dropbox(path):
    #Fetch a file from Dropbox and return it as a NumPy array.
    try:
        # Download the file from Dropbox into a byte stream
        _, res = dbx.files_download(path)
        
        # Create a byte buffer from the response content
        file_buffer = io.BytesIO(res.content)
        
        # Open the image from the byte buffer using PIL
        image = Image.open(file_buffer)
        
        # Convert the image to a NumPy array
        image_np = np.array(image)
        
        return image_np
    except dropbox.exceptions.ApiError as err:
        print(f"Error fetching file from Dropbox: {err}")
        return None


def get_photo(dolphinID,dolphin_side):
    try:
        # Construct the file path dynamically based on the dolphin ID and side
        file_path = f'/BestOfPhotos/{dolphinID}{dolphin_side}.jpg'

        # Attempt to retrieve the file from Dropbox or another source
        image_object = get_file_from_dropbox(file_path)
        
        #check if there is no photo
        if image_object is None:
            file_path = f'/BestOfPhotos/no_photo.jpg'
            image_object = get_file_from_dropbox(file_path)

        # Display the image using Streamlit, with a caption
        st.image(image_object, caption=f"Dolphin {dolphinID} ({dolphin_side})")

    except Exception as e:
        # In case of any error (e.g., file not found), show an error message
        st.error(f"Failed to retrieve image for Dolphin {dolphinID} ({dolphin_side}): {e}")

if (dolphin_id):
    get_photo(dolphin_id,side)
