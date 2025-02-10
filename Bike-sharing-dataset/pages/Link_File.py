import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

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
     
     st.image("Bike-sharing-dataset/images/fotologolink.png")
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
    
