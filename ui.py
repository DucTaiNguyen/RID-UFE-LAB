import streamlit as st
import requests

st.title("RID-UFE AI Research SaaS")

if st.button("Run Research"):

    res = requests.post("http://localhost:8000/run-research")
    data = res.json()

    st.write(data)

    st.success("Research completed")
