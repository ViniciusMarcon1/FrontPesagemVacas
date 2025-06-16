import pandas as pd
import requests 
import streamlit as st 

@st.cache_data(ttl=10)
def load_pesagens():
    response = requests.get("http://localhost:8080/api/pesagens")
    response.raise_for_status()
    return pd.DataFrame(response.json())