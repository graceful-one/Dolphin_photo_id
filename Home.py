import streamlit as st
import pandas as pd 

#import geopandas as gpd 
st.title("Home Page")

st.page_link("pages/SearchADolphin.py", label="Find A Dolphin🐬", icon="1️⃣")
st.page_link("pages/photo_query.py", label="Gallery", icon="2️⃣") 
