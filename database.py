import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection


# sheet names
sheetname_usersinfo = "users_info"
sheetname_userdata = "user_data"

# low level func

def gsheet_connect():
    # TODO: connect only if not already connected
    conn = st.connection("gsheets", type=GSheetsConnection)

def read_sheet_df(sheet_name):
    gsheet_connect()
    return conn.read(ttl=0, worksheet=sheet_name)

def overwrite_sheet_df(df, sheet_name):
    gsheet_connect()
    conn.update(data=df, worksheet=sheet_name)

def append_sheet_df(df_append, sheet_name):
    gsheet_connect()
    df = read_sheet_df(sheet_name)
    df_new = pd.concat(df, df_append, ignore_index=True)
    overwrite_sheet_df(df_new, sheet_name)


# user functions

def register_new_user(name, email, password):
    if (get_userid(email, password) is not None):
        return None
        
    df = read_sheet_df(sheetname_usersinfo)
    # columns in the Pandas Dataframe df will be:   UserID	Name	Email	Password

    max_userID = # TODO: add code here to find max of userID so far in df 
    new_userID = max_userID + 1
    new_user_df = # TODO: new df with 1 row: new_userID, name, email, password

    append_sheet_df(new_user_df, sheetname_usersinfo)

    return new_userID

def get_userid(email, password):
    # TODO: reply with userid of the user with this email if password matches
    # TODO: reply with None if no user found with this email and password

    df_new = pd.concat([df, new_row], ignore_index=True)
