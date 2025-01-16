import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
conn2 = st.connection("gsheets2", type=GSheetsConnection)

df = conn.read()
df2 = conn2.read()


st.write(df)
st.write(df2)
