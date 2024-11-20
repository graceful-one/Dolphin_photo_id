
## install packages
import streamlit as st
import pandas as pd 

#import geopandas as gpd 
st.title("Photo APP")


base_url = "https://drive.google.com/drive/folders/1fTiXUO56mvhCPjQ_BLKNh0_80npiyLqY?usp=sharing"
def get_photo_url(dolphin_id, side):
    photo_filename = f"{dolphin_id}{side}.jpg"
    return f"{base_url}{photo_filename}"

dolphin_id = st.text_input("Enter Dolphin ID (e.g., 0000a):")
side = st.radio("Select Fin Side:", ["R", "L"])

if dolphin_id:
    photo_path = get_local_photo_path(dolphin_id, side)
    if os.path.exists(photo_path):
        st.image(photo_path, caption=f"Dolphin {dolphin_id} ({side})")
    else:
        st.error("Photo not found!")
