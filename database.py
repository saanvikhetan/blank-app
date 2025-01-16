import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

#df = conn.read()
df2 = conn.read(worksheet="Sheet1")


#st.write(df)
st.write(df2)
