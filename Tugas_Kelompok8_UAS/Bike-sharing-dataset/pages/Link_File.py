import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
def load_data():
    hour = pd.read_csv("dataset/hour.csv")
    day = pd.read_csv("dataset/day.csv")
    
    # Merge data berdasarkan 'dteday'
    bike_sharing = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))
    bike_sharing['dteday'] = pd.to_datetime(bike_sharing['dteday'])
    
    # Data Cleaning
    bike_sharing.drop_duplicates(inplace=True)
    bike_sharing.dropna(inplace=True)
    
    return hour, day, bike_sharing

hour, day, bike_sharing = load_data()
st.markdown(
        "<h1 style='text-align: center;'>Link Tugas UAS</h1>",
        unsafe_allow_html=True
    )
st.write(""" 
""")

with st.sidebar:

    st.title("📌 Navigasi")
    
    page = st.radio(
        "Pilih Halaman:",
        ["🏠 Home", "🔗Link Youtube", "🔗Link Streamlit", "🔗Link Github"]
    )

if page == "🏠 Home":
    
    with st.columns(5)[2]:
     
     st.image("images/fotologolink.png")
     st.markdown(
        "<p style='text-align: center;'>Link</p>",
        unsafe_allow_html=True
    )

elif page == "🔗Link Youtube":
    st.title("🚴 Link Youtube")
    st.write("""
    **Ini Link Filenya :
    """)
    

elif page == "🔗Link Streamlit":
    st.title("🚴 Link Streamlit")
    st.write("""
    **Ini Link Filenya :
    """)
    

elif page == "🔗Link Github":
    st.title("🚴 Link Github")
    st.write("""
    **Ini Link Filenya :
    """)
    