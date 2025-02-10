import streamlit as st
import pandas as pd
import plotly.express as px

# 🔹 Fungsi Load Data
@st.cache_data
def load_data():
    hour = pd.read_csv("Bike-sharing-dataset/dataset/hour.csv")
    day = pd.read_csv("Bike-sharing-dataset/dataset/day.csv")
    bike_sharing = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))
    bike_sharing['dteday'] = pd.to_datetime(bike_sharing['dteday'])
    bike_sharing.drop_duplicates(inplace=True)
    bike_sharing.dropna(inplace=True)
    return bike_sharing

# Load dataset
bike_sharing = load_data()

# 🔹 Sidebar - Filter Data
st.sidebar.header("⚙️ Filter Data")

# Pilihan Hari dalam Seminggu (weekday_hourly)
weekdays = sorted(bike_sharing['weekday_hourly'].unique())
selected_weekdays = st.sidebar.multiselect("Pilih Hari:", weekdays, default=weekdays)

# Pilihan Musim (season_daily)
seasons = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
bike_sharing['season_name'] = bike_sharing['season_daily'].map(seasons)
selected_seasons = st.sidebar.multiselect("Pilih Musim:", seasons.values(), default=seasons.values())

# Filter berdasarkan pilihan pengguna
filtered_data = bike_sharing[
    (bike_sharing['weekday_hourly'].isin(selected_weekdays)) & 
    (bike_sharing['season_name'].isin(selected_seasons))
]

# 🔹 Pilih Variabel X & Y
selected_x = st.sidebar.selectbox("Pilih Variabel X:", bike_sharing.columns)
selected_y = st.sidebar.selectbox("Pilih Variabel Y:", bike_sharing.columns)
chart_type = st.sidebar.radio("Pilih Jenis Diagram:", ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram"])

# 🔹 Visualisasi Data yang Difilter
st.title("📊 Analisis Data Penyewaan Sepeda - Filter Interaktif")
st.subheader(f"📌 Visualisasi {chart_type} untuk '{selected_x}' vs '{selected_y}'")

if chart_type == "Scatter Plot":
    fig = px.scatter(filtered_data, x=selected_x, y=selected_y, color="season_name", title=f"Scatter Plot: {selected_x} vs {selected_y}")
elif chart_type == "Line Chart":
    fig = px.line(filtered_data, x=selected_x, y=selected_y, color="season_name", title=f"Line Chart: {selected_x} vs {selected_y}")
elif chart_type == "Bar Chart":
    fig = px.bar(filtered_data, x=selected_x, y=selected_y, color="season_name", title=f"Bar Chart: {selected_x} vs {selected_y}")
elif chart_type == "Histogram":
    fig = px.histogram(filtered_data, x=selected_x, color="season_name", title=f"Histogram: {selected_x}")

st.plotly_chart(fig)

# 🔹 Info Dataset setelah difilter
st.sidebar.markdown("---")
st.sidebar.write("📌 **Dataset yang digunakan:** `Bike Sharing`")
st.sidebar.write(f"✅ **Jumlah Data Setelah Filter**: {len(filtered_data)} baris")
st.sidebar.write(f"📊 **Jumlah Kolom**: {len(filtered_data.columns)}")
