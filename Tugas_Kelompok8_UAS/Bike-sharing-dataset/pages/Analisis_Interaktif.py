import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi Load Data
@st.cache_data
def load_data():
    hour = pd.read_csv("dataset/hour.csv")
    day = pd.read_csv("dataset/day.csv")
    bike_sharing = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))
    bike_sharing['dteday'] = pd.to_datetime(bike_sharing['dteday'])
    bike_sharing.drop_duplicates(inplace=True)
    bike_sharing.dropna(inplace=True)
    return bike_sharing

# Load dataset
bike_sharing = load_data()

# Konfigurasi Halaman
st.title("📊 Analisis Data Penyewaan Sepeda - Interaktif")

# 🔹 Sidebar untuk Pemilihan Variabel
st.sidebar.header("⚙️ Pengaturan Analisis")
selected_x = st.sidebar.selectbox("Pilih Variabel X:", bike_sharing.columns)
selected_y = st.sidebar.selectbox("Pilih Variabel Y:", bike_sharing.columns)
chart_type = st.sidebar.radio("Pilih Jenis Diagram:", ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram"])

# 🔹 Visualisasi Berdasarkan Pilihan
st.subheader(f"📌 Visualisasi {chart_type} untuk '{selected_x}' vs '{selected_y}'")

if chart_type == "Scatter Plot":
    fig = px.scatter(bike_sharing, x=selected_x, y=selected_y, title=f"Scatter Plot: {selected_x} vs {selected_y}")
elif chart_type == "Line Chart":
    fig = px.line(bike_sharing, x=selected_x, y=selected_y, title=f"Line Chart: {selected_x} vs {selected_y}")
elif chart_type == "Bar Chart":
    fig = px.bar(bike_sharing, x=selected_x, y=selected_y, title=f"Bar Chart: {selected_x} vs {selected_y}")
elif chart_type == "Histogram":
    fig = px.histogram(bike_sharing, x=selected_x, title=f"Histogram: {selected_x}")

# Tampilkan diagram
st.plotly_chart(fig)

# Info Dataset
st.sidebar.markdown("---")
st.sidebar.write("📌 **Dataset yang digunakan:** `Bike Sharing`")
st.sidebar.write(f"✅ **Jumlah Data**: {len(bike_sharing)} baris")
st.sidebar.write(f"📊 **Jumlah Kolom**: {len(bike_sharing.columns)}")