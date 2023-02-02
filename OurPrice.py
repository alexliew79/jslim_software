
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import numpy as np

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


# configure the streamlit app
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart", layout="wide")
st.title("Price Estimate:")

#st.write(
#    """This app accomodates the blog [here](<https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/>)
#    and walks you through one example of how the Streamlit
#    Data Science Team builds add-on functions to Streamlit.
#    """
#)
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a UI on top of a dataframe to let viewers filter columns

        Args:
            df (pd.DataFrame): Original dataframe

        Returns:
            pd.DataFrame: Filtered dataframe
        """
        modify = st.checkbox("Add filters")

        if not modify:
            return df

        # Make a copy of the pandas dataframe so the user input will not change the underlying data
        df = df.copy()

        # Try to convert datetimes into a standard format (datetime, no timezone)
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        # create an instance of container
        modification_container = st.container()

        # adding filtering widgets into the container dependent on datatype
        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                left.write("↳")
                # Treat columns with < 10 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Values for {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    user_text_input = right.text_input(
                        f"Keyword Search: {column}",
                    )
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input[0].upper() + user_text_input[1:].lower())]

        return df

#reading our data frame
df = pd.read_excel(io = "v3.xlsx",
                      engine = "openpyxl",
                      sheet_name = "Single",
                      skiprows = 0
                        )

#drop rows with complete nan
df = df.dropna(how="all")

#drop rows with empty date
df = df.dropna(subset=["Date"])

#drop any rows that have been accidentally duplicated
#df = df.duplicated(keep=False) #subset[""], using all rows now

#by right, I want the latest date only. But having different prices at different date
#can help me see any difference
#df.groupby([]).sort(["date"]).tail(1)

#drop rows with empty date
#df = df.drop("Date", inplace=True)

df = df.rename(columns={"MU-MIN": "MU-Min"})

#convert prices to numeric
df["Min"] = pd.to_numeric(df["Min"], errors="coerce")
df["Max"] = pd.to_numeric(df["Max"], errors="coerce")
df["MU-Min"] = pd.to_numeric(df["MU-Min"], errors="coerce")
df["MU-Max"] = pd.to_numeric(df["MU-Max"], errors="coerce")

#Check price column now
#col_to_check = ["Min", "Max", "MU-Min", "MU-Max"]
#df = df.dropna(subset=col_to_check, how="all", inplace=True)

df.fillna("", inplace=True)

st.sidebar.header("Please filter here:")
In = st.sidebar.multiselect(
    "Choose Area of Work:",
    options=df["In"].unique(),
    default=df["In"].unique()
)


#def_col = [x for x in df.columns if (x!="Date" or x!="Contact" or x!="Supplier")]
def_col = list(df.columns)
def_col.remove("Contact")
def_col.remove("Date")
def_col.remove("Supplier")

wts = st.sidebar.multiselect(
    "Choose Colums to Display:",
    options=df.columns,
    default=def_col
    #list(df.columns).remove("Contact").remove("Supplier").remove("Date") #list(df.columns).remove("Date","Contact","Supplier")#["Notes", "Purpose", "Composition", "In", "On", "Work 1", "Work 2", "Material", "What", "Measurement", "Min", "Max", "MU-MIN", "MU-Max"]
)

#select dataframe base on user selection
#df_selection = df.query("In==@In")# & Part_Of==@part_of & Type==@work_type")


#select columns based on user preference
df_selection = df.query("In==@In")# & Part_Of==@part_of & Type==@work_type")

df_selection = df_selection.loc[:, wts]
#adding a subheader in the main page
st.subheader(f'Area Displayed: :blue{In}') #:blue[colors] and emojis :sunglasses:')
st.dataframe(filter_dataframe(df_selection))
