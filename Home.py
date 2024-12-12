import streamlit as st
import pandas as pd 

#import geopandas as gpd 
st.title("Home Page")

st.page_link("pages/SearchADolphin.py", label="Find A Dolphin🐬", icon="1️⃣")
st.markdown("<p style='color:grey; margin-left: 100px;'>---Find information by dolphin ID</p>", unsafe_allow_html=True)

st.page_link("pages/photo_query.py", label="Gallery", icon="2️⃣") 
st.markdown("<p style='color:grey; margin-left: 100px;'>---If you only looking for the fin photo</p>", unsafe_allow_html=True)

st.page_link("pages/add-dolphin.py", label="Add A Dolphin", icon="3️⃣") 
st.markdown("<p style='color:grey; margin-left: 100px;'>---Add your dolphin observations</p>", unsafe_allow_html=True)
