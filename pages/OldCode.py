import pandas as pd
import numpy as np

import plotly.express as px
import streamlit as st

# configure the streamlit app
st.set_page_config(page_title="Price Dashboard", page_icon=":bar_chart", layout="wide")
st.title("Prices By Work Area")

#reading our data frame
df = pd.read_excel(io = "v3.xlsx",
                      engine = "openpyxl",
                      sheet_name = "Notes",
                      skiprows = 0
                        )
#drop rows with complete nan
df = df.dropna(how="all")

#drop rows with empty date
df = df.dropna(subset=["Date"])

#convert prices to numeric
df["Customer Price (Min)"] = pd.to_numeric(df["Customer Price (Min)"], errors="coerce").fillna(0)
df["Customer Price (Max)"] = pd.to_numeric(df["Customer Price (Max)"], errors="coerce").fillna(0)

#renaming
df.rename(columns={"Part Of": "Part_Of"}, inplace = True)

#list to append str only type
#tab_labels = []

#check type and append to list
#for item in df["Area"].unique().tolist():
#    if type(item) == str:
#        tab_labels.append(item)
#    else:
#        continue

#counter to loop tab_labels
#tab_counter = 0

#to display selected dataframe
#for tab in st.tabs(tab_labels):
#    df_selection = df.loc[df.Area == tab_labels[tab_counter], :]
#    st.dataframe(df_selection)
#    tab_counter += 1


#tabs = st.tabs(tab_labels) #["Kitchen","Living Room")

#tab_type = tabs[0]

#sub_df = df.loc[df["Area"]=="Kitchen", :]

#with tab_type:

#    st.dataframe(sub_df)

#filter by area of home
st.sidebar.header("Please filter here:")
area = st.sidebar.multiselect(
    "Choose Area of Work:",
    options=df["Area"].unique(),
    default=df["Area"].unique()

)

#filter by where the work belong to
#part_of = st.sidebar.multiselect(
#    "Choose Category of work:",
#    options=df["Part_Of"].unique(),
#    default=df["Part_Of"].unique()

#)

#filter by standard or custom
#work_type = st.sidebar.multiselect(
#    "Choose Custom or Standard:",
#    options=df["Type"].unique(),
#    default=df["Type"].unique()
#)

#select dataframe base on user selection
df_selection = df.query("Area==@area")# & Part_Of==@part_of & Type==@work_type")

#display in browser
st.dataframe(df_selection)

st.title(":bar_chart: Pricing Dashboard")

#st.markdown()

#'''
