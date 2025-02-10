import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Load data

# Sidebar
with st.sidebar:
    st.title("📌 Navigasi")
    page = st.radio(
        "Pilih Halaman:",
        ["🏠 Home", "👥 Anggota Kelompok dan Kontribusi"]
    )


if page == "🏠 Home":
    # Membuat judul dan teks di tengah
    st.markdown(
        "<h1 style='text-align: center;'>🚴 Selamat Datang di Identitas Lanjutan Kelompok</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center;'>Project ini dibuat untuk memenuhi tugas UAS Pemrograman Dasar Sains Data</p>",
        unsafe_allow_html=True
    )
    
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologokelompok.png")
     st.markdown(
        "<p style='text-align: center;'>Kelompok 8</p>",
        unsafe_allow_html=True
    )


elif page == "👥 Anggota Kelompok dan Kontribusi":
    st.title("👥 Anggota Kelompok dan Kontribusi")
    st.write("""
    **Kontribusi Per Orang Membuat Tugas UAS (%):**
    - 👤 **10123022 - Muhamad Nauval. P** - 20% :
        - Membuat soal 3
        - Membuat Logo            
    - 👤 **10123027 - M. Ilyas Fachrezy Nur'Ichsan** - 20% :
        - Membuat soal 4
        - Membuat Text Untuk Video  
    - 👤 **10123030 - Muhammad Rizki** - 40% :
        - Membuat file ipynb
        - Membuat file py
        - Membuat tampilan aplikasi di Streamlit
        - Membuat soal 1 dan 2
        - Membuat page 1 (yang didalamnya ada )
        - Membuat page 2 (yang didalamnya ada 🏠 Home, 📊 Data Analysis, 👥 Kontribusi, ❓ Pertanyaan, 🧾 Jawaban)
        - Membuat page 3 (yang didalamnya ada 🏠 Home, 📊 Analisis Regresi Penyewaan Sepeda, 📊 Analisis Time Series: Tren Penyewaan Sepeda, 📊 Analisis Variansi (ANOVA), 📍 Geoanalysis, 🧠 Data Mining: Clustering Penyewaan Sepeda, 🧠 Data Mining: Clustering & Analisis Diskriminan)
        - Membuat page 4 (yang didalamnya ada 🏠 Home, 👥 Anggota Kelompok dan Kontribusi)
    - 👤 **10123031 - Ahmad Maulana Ramdani** - 10% 
        - Membuat soal 6
    - 👤 **10123041 - Muhammad Rizki Aliansyah** - 10%
        - Membuat soal 5
    
    
    **Untuk penjelasan kontribusi lebih lanjut dapat dilihat pada page Identitas📖**
    """)
