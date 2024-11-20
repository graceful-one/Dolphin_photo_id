import streamlit as st
import pandas as pd 

#import geopandas as gpd 
st.title("Home Page")

st.page_link("pages/Dolphin_query.py", label="dolphin query", icon="1️⃣")
st.page_link("pages/photo_query.py", label="photo query", icon="2️⃣") 
