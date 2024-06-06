import time
import streamlit as st
import pandas as pd
import numpy as np 

st.set_page_config(page_title="Consumption", page_icon="📈")

conn = st.connection("mysql", type="sql")
df = conn.query("SELECT DATE_FORMAT(timestamp, '%H:%i:%s') as timestamp, units FROM consumption ORDER BY units ASC")

df = df[['units', 'timestamp']]
df = df.set_index('timestamp')

df['units'] = df['units'].values[::-1]
st.markdown("""
# Consumption Levels 📈
---
            """)
st.write("This page shows the Consumption levels against time")
st.write(df.head())
st.line_chart(df)
