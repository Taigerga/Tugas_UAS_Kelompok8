import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import folium
import scipy.stats as stats
from streamlit_folium import folium_static
from sklearn_extra.cluster import KMedoids
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly import graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import streamlit_folium
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    hour = pd.read_csv("Bike-sharing-dataset/dataset/hour.csv")
    day = pd.read_csv("Bike-sharing-dataset/dataset/day.csv")
    
    # Merge data berdasarkan 'dteday'
    bike_sharing = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))
    bike_sharing['dteday'] = pd.to_datetime(bike_sharing['dteday'])
    
    # Data Cleaning
    bike_sharing.drop_duplicates(inplace=True)
    bike_sharing.dropna(inplace=True)
    
    return hour, day, bike_sharing

hour, day, bike_sharing = load_data()

st.markdown(
        "<h1 style='text-align: center;'>Analisis Lanjutan</h1>",
        unsafe_allow_html=True
    )

# Sidebar
with st.sidebar:
    st.title("📌 Navigasi")
    page = st.radio(
        "Pilih Halaman:",
        ["🏠 Home", "📊 Analisis Regresi Penyewaan Sepeda", "📊 Analisis Time Series: Tren Penyewaan Sepeda", "📊 Analisis Variansi (ANOVA)", "📍 Geoanalysis", "🧠 Data Mining: Clustering Penyewaan Sepeda","🧠 Data Mining: Clustering & Analisis Diskriminan"]
    )

if page == "🏠 Home":
    st.title("🚴 Selamat Datang di Bike Sharing Data Analysis Lanjutan")
    st.write("""
    **Aplikasi ini dirancang untuk menganalisis data penyewaan sepeda berdasarkan berbagai faktor secara tingkat lanjut.**
    Silakan gunakan navigasi di sidebar untuk menjelajahi berbagai analisis yang tersedia.
    """)
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologosepeda2.png")
     st.markdown(
        "<p style='text-align: center;'>Sepeda</p>",
        unsafe_allow_html=True
    )


# 📊 Data Analysis
elif page == "📊 Analisis Regresi Penyewaan Sepeda":
    st.title("📊 Analisis Regresi Penyewaan Sepeda")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologoanalisis.png")
     st.markdown(
        "<p style='text-align: center;'>Analisis</p>",
        unsafe_allow_html=True
    )
    # Gunakan data dari bike_sharing
    X = bike_sharing[['temp_hourly', 'hum_hourly', 'windspeed_hourly']]
    y = bike_sharing['cnt_hourly']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model Linear Regression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # Prediksi
    y_pred = regressor.predict(X_test)

    # Evaluasi Model
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.subheader("📊 Evaluasi Model Regresi Linear")
    st.write(f"🎯 Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"📈 R-squared: {r2:.2f}")

    # Visualisasi
    st.subheader("📉 Prediksi vs Aktual")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_test, y=y_pred, mode='markers', 
                            marker=dict(color='blue', opacity=0.6), 
                            name='Prediksi'))
    fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], 
                            mode='lines', line=dict(color='red', dash='dash'), 
                            name='Garis Ideal'))

    fig.update_layout(
        title="Prediksi vs Nilai Aktual",
        xaxis_title="Nilai Aktual",
        yaxis_title="Nilai Prediksi",
        template="plotly_dark",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


elif page == "📊 Analisis Time Series: Tren Penyewaan Sepeda":
    st.title("📊 Analisis Time Series: Tren Penyewaan Sepeda")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologoanalisis.png")
     st.markdown(
        "<p style='text-align: center;'>Analisis</p>",
        unsafe_allow_html=True
    )

    # Agregasi data berdasarkan tanggal
    bike_daily = bike_sharing.groupby('dteday').agg({'cnt_hourly': 'sum'}).reset_index()
    bike_daily.rename(columns={'cnt_hourly': 'total_rentals'}, inplace=True)

    # Plot Tren Penyewaan
    st.subheader("📈 Tren Penyewaan Sepeda Harian")
    fig = px.line(bike_daily, x='dteday', y='total_rentals', title="Tren Penyewaan Sepeda")
    st.plotly_chart(fig)

    # **Seasonal Decomposition**
    st.subheader("📊 Seasonal Decomposition")

    # Set index ke tanggal
    bike_daily.set_index("dteday", inplace=True)

    # Lakukan dekomposisi musiman
    decomposition = seasonal_decompose(bike_daily['total_rentals'], model='additive', period=30)

    # Buat figure untuk Plotly
    fig = go.Figure()

    # Tambahkan komponen tren
    fig.add_trace(go.Scatter(x=bike_daily.index, y=decomposition.trend, mode='lines', name='Trend'))

    # Tambahkan komponen musiman
    fig.add_trace(go.Scatter(x=bike_daily.index, y=decomposition.seasonal, mode='lines', name='Seasonal'))

    # Tambahkan komponen residu
    fig.add_trace(go.Scatter(x=bike_daily.index, y=decomposition.resid, mode='lines', name='Residual'))

    # Layout
    fig.update_layout(
        title="Seasonal Decomposition",
        xaxis_title="Tanggal",
        yaxis_title="Total Penyewaan",
        template="plotly_dark",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Tampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # **Prediksi dengan ARIMA**
    st.subheader("🔮 Prediksi Penyewaan Sepeda dengan ARIMA")
    
    # Train ARIMA
    model = ARIMA(bike_daily['total_rentals'], order=(5,1,2))
    model_fit = model.fit()
    
    # Prediksi 30 hari ke depan
    forecast = model_fit.forecast(steps=30)
    future_dates = pd.date_range(start=bike_daily.index[-1], periods=30, freq='D')

    # Visualisasi
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bike_daily.index, y=bike_daily['total_rentals'], mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode='lines', name='Forecast', line=dict(dash='dot')))
    
    st.plotly_chart(fig)


# 📊 **Analisis Variansi (ANOVA)**
elif page == "📊 Analisis Variansi (ANOVA)":
    # **Analisis Variansi (ANOVA)**
    st.title("📊 Analisis Variansi (ANOVA)")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologoanalisis.png")
     st.markdown(
        "<p style='text-align: center;'>Analisis</p>",
        unsafe_allow_html=True
    )
     
    # **ANOVA untuk Hari dalam Seminggu**
    st.write("### 🗓️ Apakah ada perbedaan signifikan dalam penyewaan sepeda berdasarkan hari dalam seminggu?")

    weekend = bike_sharing[bike_sharing['weekday_hourly'].isin([0, 6])]['cnt_hourly']
    weekday = bike_sharing[bike_sharing['weekday_hourly'].isin([1, 2, 3, 4, 5])]['cnt_hourly']

    # Uji ANOVA
    anova_week = stats.f_oneway(weekend, weekday)

    # Hasil
    st.write(f"📌 **Nilai F:** {anova_week.statistic:.2f}, **p-value:** {anova_week.pvalue:.4f}")
    if anova_week.pvalue < 0.05:
        st.write("✅ Terdapat perbedaan signifikan antara hari kerja dan akhir pekan.")
    else:
        st.write("❌ Tidak ada perbedaan signifikan antara hari kerja dan akhir pekan.")

    # Visualisasi
    fig_week = px.box(bike_sharing, x="weekday_hourly", y="cnt_hourly", 
                    title="Distribusi Penyewaan Sepeda Berdasarkan Hari dalam Seminggu",
                    labels={"weekday_hourly": "Hari dalam Seminggu", "cnt_hourly": "Jumlah Penyewaan"},
                    color="weekday_hourly")
    st.plotly_chart(fig_week, use_container_width=True)

    # **ANOVA untuk Kategori Suhu**
    st.write("### 🌡️ Apakah suhu mempengaruhi penyewaan sepeda?")

    bins = [bike_sharing["temp_hourly"].min(), 0.2, 0.4, 0.6, 0.8, bike_sharing["temp_hourly"].max()]
    labels = ["Sangat Dingin", "Dingin", "Sedang", "Hangat", "Panas"]
    bike_sharing["temp_category"] = pd.cut(bike_sharing["temp_hourly"], bins=bins, labels=labels)

    # Data berdasarkan kategori suhu
    temp_groups = [bike_sharing[bike_sharing["temp_category"] == cat]["cnt_hourly"] for cat in labels]

    # Uji ANOVA
    anova_temp = stats.f_oneway(*temp_groups)

    st.write(f"📌 **Nilai F:** {anova_temp.statistic:.2f}, **p-value:** {anova_temp.pvalue:.4f}")
    if anova_temp.pvalue < 0.05:
        st.write("✅ Terdapat perbedaan signifikan antara kategori suhu.")
    else:
        st.write("❌ Tidak ada perbedaan signifikan antara kategori suhu.")

    # Visualisasi
    fig_temp = px.box(bike_sharing, x="temp_category", y="cnt_hourly", 
                    title="Distribusi Penyewaan Sepeda Berdasarkan Kategori Suhu",
                    labels={"temp_category": "Kategori Suhu", "cnt_hourly": "Jumlah Penyewaan"},
                    color="temp_category")
    st.plotly_chart(fig_temp, use_container_width=True)

# 🧠 Data Mining (Clustering)
elif page == "🧠 Data Mining: Clustering Penyewaan Sepeda":
    st.title("🧠 Data Mining: Clustering Penyewaan Sepeda")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologobuku.png")
     st.markdown(
        "<p style='text-align: center;'>Data Mining</p>",
        unsafe_allow_html=True
    )
    # **Pilih fitur untuk clustering**
    st.subheader("🎯 K-Means Clustering")
    clustering_data = bike_sharing[['temp_hourly', 'hum_hourly', 'windspeed_hourly', 'cnt_hourly']]
    scaler = StandardScaler()
    clustering_scaled = scaler.fit_transform(clustering_data)

    # **Menentukan jumlah cluster optimal dengan metode elbow**
    distortions = []
    K_range = range(1, 11)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(clustering_scaled)
        distortions.append(kmeans.inertia_)

    # Visualisasi elbow method menggunakan Plotly
    fig_elbow = go.Figure()
    fig_elbow.add_trace(go.Scatter(x=list(K_range), y=distortions, mode='lines+markers',
                                marker=dict(size=8, color='red'), line=dict(color='blue')))
    fig_elbow.update_layout(title='Metode Elbow', xaxis_title='Jumlah Cluster',
                            yaxis_title='Distortion (Inertia)', template='plotly_white')
    st.plotly_chart(fig_elbow, use_container_width=True)


    # Clustering dengan K=3
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    bike_sharing["cluster"] = kmeans.fit_predict(clustering_scaled)

    # Visualisasi hasil clustering
    fig = px.scatter_3d(bike_sharing, x='temp_hourly', y='hum_hourly', z='cnt_hourly', 
                         color=bike_sharing["cluster"].astype(str), title="Cluster Penyewaan Sepeda")
    st.plotly_chart(fig)

    # **K-Medoids Clustering**
    st.subheader("🔍 K-Medoids Clustering")

    kmedoids = KMedoids(n_clusters=3, random_state=42)
    bike_sharing["cluster_kmedoids"] = kmedoids.fit_predict(clustering_scaled)

    # Visualisasi K-Medoids
    fig = px.scatter_3d(bike_sharing, x='temp_hourly', y='hum_hourly', z='cnt_hourly', 
                         color=bike_sharing["cluster_kmedoids"].astype(str), title="K-Medoids Clustering")
    st.plotly_chart(fig)

elif page == "🧠 Data Mining: Clustering & Analisis Diskriminan":
    st.title("🧠 Data Mining: Clustering & Analisis Diskriminan")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologobuku.png")
     st.markdown(
        "<p style='text-align: center;'>Data Mining</p>",
        unsafe_allow_html=True
    )
    # Pilih fitur dan target untuk LDA
    X_lda = bike_sharing[['temp_hourly', 'hum_hourly', 'windspeed_hourly']]  # Fitur
    y_lda = bike_sharing['season_daily']  # Target klasifikasi (kategori musim)

    # Standardisasi data
    scaler = StandardScaler()
    X_lda_scaled = scaler.fit_transform(X_lda)

    # LDA
    lda = LinearDiscriminantAnalysis(n_components=2)  # Ubah n_components sesuai kebutuhan
    X_lda_transformed = lda.fit_transform(X_lda_scaled, y_lda)

    # Cek jumlah komponen yang dihasilkan
    num_components = X_lda_transformed.shape[1]
    lda_columns = [f"LD{i+1}" for i in range(num_components)]  # LD1, LD2, dst.

    # Buat DataFrame LDA
    lda_df = pd.DataFrame(X_lda_transformed, columns=lda_columns)
    lda_df["Category"] = y_lda.values  # Tambahkan kategori penyewaan

    # Tampilkan DataFrame untuk memastikan tidak ada error
    st.write(lda_df.head())

    # Visualisasi LDA
    if num_components > 1:
        st.subheader("📈 Visualisasi LDA (LD1 vs LD2)")
        fig = px.scatter(lda_df, x="LD1", y="LD2", color=lda_df["Category"].astype(str),
                         title="Visualisasi Analisis Diskriminan Linear (LDA)",
                         labels={"LD1": "Linear Discriminant 1", "LD2": "Linear Discriminant 2"},
                         template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.subheader("📈 Distribusi LDA")
        fig = px.histogram(lda_df, x="LD1", color=lda_df["Category"].astype(str), barmode="overlay",
                           title="Distribusi Kategori Penyewaan Sepeda berdasarkan LD1")
        st.plotly_chart(fig)
    


# 📍 Geoanalysis (Visualisasi Lokasi Stasiun Sepeda)
elif page == "📍 Geoanalysis":
    st.title("📍 Geoanalysis: Peta Stasiun Penyewaan Sepeda")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologoglobe.png")
     st.markdown(
        "<p style='text-align: center;'>Map</p>",
        unsafe_allow_html=True
    )
    stations = pd.DataFrame({
        "Station": ["Stasiun A", "Stasiun B", "Stasiun C"],
        "Latitude": [-6.914744, -6.917464, -6.921024],
        "Longitude": [107.609810, 107.620590, 107.630260],
        "Total Rides": [5000, 8000, 6000]
    })

    st.subheader("📌 Lokasi Stasiun Sepeda")
    bike_map = folium.Map(location=[-6.917464, 107.620590], zoom_start=14)

    for _, row in stations.iterrows():
        folium.Marker([row["Latitude"], row["Longitude"]], 
                      popup=f"{row['Station']}: {row['Total Rides']} rides",
                      icon=folium.Icon(color="blue", icon="bicycle")).add_to(bike_map)

    folium_static(bike_map)

    # Heatmap lokasi penyewaan tinggi
    st.subheader("🔥 Heatmap Penyewaan Sepeda")
    fig = px.density_mapbox(stations, lat="Latitude", lon="Longitude", z="Total Rides",
                            radius=20, center=dict(lat=-6.917464, lon=107.620590),
                            zoom=13, mapbox_style="open-street-map",
                            title="Heatmap Penyewaan Sepeda")
    st.plotly_chart(fig)
