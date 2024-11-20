## install packages
import streamlit as st
import pandas as pd 

#import geopandas as gpd 
st.title("Dolphin Query")

##load dolphin database
try:
    dolphin_df = pd.read_csv(r"tblDolphin.csv",
                            index_col="Dolphin_ID_Number",
                            encoding="ISO-8859-1")
    observations_df = pd.read_csv(r"tblDolphinsObserved.csv", encoding="ISO-8859-1")
except UnicodeDecodeError:
    st.error("There was an error reading the file due to encoding issues.")
except FileNotFoundError:
    st.error("The file was not found at the specified path.")

## Set up dictionaries of meanings - idk if i actually need to do this

## Take in user input of which dolphin  
search_dolphin = "4445a" # hard coding for now will figure out the input later
st.write(dolphin_df.head())
## Search dataframe of observations for all sightings of that dolphin  
dolphin_data = dolphin_df.loc[[search_dolphin]]

## Create new dataframe of the dates of those sightings  

## Print basic dolphin information  
st.write("Date of first observation: "+ str(dolphin_data["Dolphin_First_Observed"].item()))
## Print out table of dates of observations 
