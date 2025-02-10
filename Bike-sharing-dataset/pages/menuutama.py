import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.markdown(
        "<h1 style='text-align: center;'>Menu Utama</h1>",
        unsafe_allow_html=True
    )
st.markdown(
        "<h1 style='text-align: center;'>🚴 Selamat Datang di Aplikasi Bike Sharing Data Analysis</h1>",
        unsafe_allow_html=True
    )

with st.columns(5)[2]:
    st.image("Bike-sharing-dataset/images/fotologosepeda.png")
    st.markdown(
        "<p style='text-align: center;'>Sepeda</p>",
        unsafe_allow_html=True
    )



with st.sidebar:
    # Add logo
    
    col1, col2, col3 = st.columns([1, 3, 1])  # Buat 3 kolom, kolom tengah lebih besar
    with col2:  # Taruh gambar di kolom tengah
        st.image("Bike-sharing-dataset/images/logo_unikom_kuning.png", caption="Universitas Komputer Indonesia", use_container_width=True)

    # Multipage navigation
    st.markdown("### 👥 Tugas Kelompok UAS")
    st.write("""
    - **👤 10123022 - Muhamad Nauval. P
    - **👤 10123027 - M. Ilyas Fachrezy Nur'Ichsan
    - **👤 10123030 - Muhammad Rizki  
    - **👤 10123031 - Ahmad Maulana Ramdani 
    - **👤 10123041 - Muhammad Rizki Aliansyah  
    """)
