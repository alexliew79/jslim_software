import pandas
import streamlit as st
import pandas as pd

#reading our data frame
df = pd.read_excel(io = "v3.xlsx",
                      engine = "openpyxl",
                      sheet_name = "Value Definition"
                        )

# Create a sample dataframe
#df = pd.DataFrame({'Package': ['Restoration', 'Structural', 'Others'],
#                   'Purpose': ['Standard', 'Custom', 'Others'],
#                   'Description': ['Hacking - Demolish', 'Laying', 'Delivery - Disposal']})

# Create a function to save data to excel
def save_to_excel(df, filename):
    df.to_excel(filename)

# Create a function to select columns
#def select_columns():
#    selected_columns = st.multiselect("Select columns", df.columns)
#    return df[selected_columns]

def select_columns():
    selected_columns = []
    for column in df.columns:
        selected_column = st.selectbox(f"Select a value for {column}", df[column].unique())
        selected_columns.append(selected_column)
    return selected_columns

# Create a function to take user input
def user_input():
    user_input = st.text_input("Add a note")
    df['Notes'] = user_input
    return df

def app(df):
    st.title("Streamlit App")
    cols = df.columns
#    selected_cols = select_columns()
    selected_cols = [st.sidebar.selectbox(label, df.columns.unique(), format_func=lambda x: f'{x[:10]}...') for label, col
                     in zip(cols, cols)]

    st.markdown("hello " + selected_cols[0] + "")


def app(df):
    st.title("Streamlit App")

    cols = ['col1', 'col2', 'col3']

    sub_df = df[
        (df[cols[0]] == selected_cols[0]) & (df[cols[1]] == selected_cols[1]) & (df[cols[2]] == selected_cols[2])]
    st.dataframe(sub_df)


if __name__ == '__main__':
    app(df)

# Use the full page instead of a narrow central column
st.set_page_config(layout = "wide")

# Space out the maps so the first one is 2x the size of the other three
#c1, c2, c3, c4 = st.columns((2, 1, 1, 1))


if __name__ == '__main__':
    app(df)
