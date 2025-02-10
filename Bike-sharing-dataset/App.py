import os
print(os.getcwd())

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Set page title and icon
st.set_page_config(page_title="🚴 Bike Sharing Data Analysis", page_icon="🚴‍♂️", layout="wide")

# Define pages
lanjutan_analisis_page = st.Page(
    page="pages/LanjutanAnalisis.py",
    title="Analisis Lanjutan 📉",
    
)

identitas_page = st.Page(
    page="pages/Identitas.py",
    title="Identitas Kelompok 👤"
)

Analisis_Sederhana_page = st.Page(
    page="pages/AnalisisSederhana.py",
    title="Analisis Sederhana 📈"
)

hal_menu_utama = st.Page(
    page="pages/menuutama.py",
    title="Menu Utama 📝",
    default=True
)

hal_link_file = st.Page(
    page="pages/Link_File.py",
    title="Link Tugas UAS 🌐"
)

Analisis_Interaktif_page = st.Page(
    page="pages/Analisis_Interaktif.py",
    title="Analisis Interaktif 🌐"
)

Analisis_Filter_page = st.Page(
    page="pages/Analisis_Filter.py",
    title="Analisis Filter 🌐"
)

# Set up navigation
#pg = st.navigation(pages=[hal_menu_utama, Analisis_Sederhana_page, lanjutan_analisis_page, identitas_page, hal_link_file])
pg = st.navigation(
    {
        "Menu Utama Aplikasi": [hal_menu_utama],
        "Analisis Bike Sharing": [Analisis_Sederhana_page, lanjutan_analisis_page, Analisis_Interaktif_page, Analisis_Filter_page],
        "Identitas": [identitas_page],
        "Tautan File": [hal_link_file]
    }
)
pg.run()

