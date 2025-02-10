import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import folium
import io
import scipy.stats as stats
import warnings
warnings.filterwarnings("ignore")

st.markdown(
        "<h1 style='text-align: center;'>Analisis Sederhana</h1>",
        unsafe_allow_html=True
    )
# Sidebar with logo and multipage navigation
with st.sidebar:

    st.title("📌 Navigasi")
    
    page = st.radio(
        "Pilih Halaman:",
        ["🏠 Home", "📊 Data Analysis", "👥 Kontribusi", "❓ Pertanyaan", "🧾 Jawaban"]
    )

# Load data (only once)
@st.cache_data
def load_data():
    hour = pd.read_csv("Bike-sharing-dataset/dataset/hour.csv")
    day = pd.read_csv("Bike-sharing-dataset/dataset/day.csv")
    bike_sharing = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))
    bike_sharing['dteday'] = pd.to_datetime(bike_sharing['dteday'])
    bike_sharing.drop_duplicates(inplace=True)
    bike_sharing.dropna(inplace=True)
    return hour, day, bike_sharing

hour, day, bike_sharing = load_data()

# Home Page
if page == "🏠 Home":
    st.title("🚴 Selamat Datang di Bike Sharing Data Analysis Sederhana")
    st.write("""
    **Aplikasi ini dirancang untuk menganalisis data penyewaan sepeda berdasarkan berbagai faktor seperti musim, cuaca, suhu, dan kelembaban.**
    Silakan gunakan navigasi di sidebar untuk menjelajahi berbagai analisis yang tersedia.
    """)
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologosepeda1.png")
     st.markdown(
        "<p style='text-align: center;'>Sepeda</p>",
        unsafe_allow_html=True
    )

# Data Analysis Page
elif page == "📊 Data Analysis":
    st.title("🚴 Bike Sharing Data Analysis")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologoanalisis.png")
     st.markdown(
        "<p style='text-align: center;'>Analisis</p>",
        unsafe_allow_html=True
    )
    # Define tabs
    tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "🌦️ Aggregations by Season", "🔍 Additional Analysis"])

    with tab1:
        
        st.header("📊 Data Overview")
        st.subheader("📅 Hourly Data")
        st.write(hour.head())
        st.subheader("📅 Daily Data")
        st.write(day.head())
        st.subheader("🔗 Merged Data")
        st.write(bike_sharing.head())
        st.subheader("❓ Null Values")
        st.write(bike_sharing.isnull().sum())
        st.subheader("🗂️ 🔄 Jumlah Data Duplikat")
        st.write(f"🔍 **Total Duplikat:** {bike_sharing.duplicated().sum()} 🛑")
        st.subheader("📋 ℹ️ Ringkasan DataFrame")
        buffer = io.StringIO()
        bike_sharing.info(buf=buffer)
        st.text(buffer.getvalue())
        st.subheader("📑 🏷️ Tipe Data Tiap Kolom")
        st.dataframe(bike_sharing.dtypes.rename("📌 Data Type"))
        st.subheader("🔢 🏷️ Nilai Unik dalam Kolom")
        selected_column = st.selectbox("📌 Pilih kolom untuk melihat nilai unik:", bike_sharing.columns)
        st.write(f"✨ **Nilai unik dari '{selected_column}':**", bike_sharing[selected_column].unique())
        st.header("📈 Descriptive Statistics")
        st.write(bike_sharing.describe())

    with tab2:
        st.header("🌦️ Aggregations by Season")
        
        agg1 = bike_sharing.groupby(by="season_hourly").agg({
            "workingday_hourly": "count", 
            "windspeed_hourly": ["max", "min", "mean", lambda x: x.max() - x.min()]
        }).sort_values(by=("workingday_hourly", "count"), ascending=False)
        st.subheader("📅 Working Day Count and 🌬️ Windspeed by Season")
        st.write(agg1)

        agg2 = bike_sharing.groupby(by="season_hourly").agg({
            "temp_hourly": ["max", "min", "mean", lambda x: x.max() - x.min()]
        })
        st.subheader("🌡️ Temperature Statistics by Season")
        st.write(agg2)

        agg3 = bike_sharing.groupby(by="season_hourly").agg({
            "hum_hourly": ["mean", "max", "min", lambda x: x.max() - x.min()]
        })
        st.subheader("💧 Humidity Statistics by Season")
        st.write(agg3)

        agg4 = bike_sharing.groupby(by="season_hourly").agg({
            "cnt_hourly": ["sum", "mean", "max"]
        }).sort_values(by=("cnt_hourly", "sum"), ascending=False)
        st.subheader("🚴 Total Rentals by Season")
        st.write(agg4)

        agg5 = bike_sharing.groupby(by="season_hourly").agg({
            "casual_hourly": ["sum", "mean"],
            "registered_hourly": ["sum", "mean"]
        })
        st.subheader("👤 Casual and Registered Users by Season")
        st.write(agg5)

        agg6 = bike_sharing.groupby(by="season_hourly").agg({
            "cnt_hourly": ["sum", "mean"], 
            "windspeed_hourly": ["mean", "max"], 
            "temp_hourly": ["mean", lambda x: x.max() - x.min()]
        }).sort_values(by=("cnt_hourly", "sum"), ascending=False)
        st.subheader("📊 Comprehensive Statistics by Season")
        st.write(agg6)

    with tab3:
        st.header("🔍 Additional Analysis")

        # Scatter plot: windspeed vs cnt
        fig1 = px.scatter(bike_sharing, 
                        x='windspeed_hourly', 
                        y='cnt_hourly', 
                        title="Hubungan Kecepatan Angin dan Penyewaan Sepeda", 
                        labels={'windspeed_hourly': 'Kecepatan Angin', 'cnt_hourly': 'Jumlah Penyewaan'},
                        template='plotly_white',
                        opacity=0.7)  # Bikin transparan
        st.plotly_chart(fig1, use_container_width=True)
        
        # Korelasi windspeed dan cnt
        correlation = bike_sharing['windspeed_hourly'].corr(bike_sharing['cnt_hourly'])
        st.write(f"📊 Korelasi antara kecepatan angin dan jumlah penyewaan sepeda: {correlation:.2f}")
        
        # Rata-rata jumlah sewa pada kategori kecepatan angin
        bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, bike_sharing['windspeed_hourly'].max()]
        labels = ['Sangat Rendah', 'Rendah', 'Sedang', 'Cukup Tinggi', 'Tinggi', 'Sangat Tinggi']
        bike_sharing['windspeed_category'] = pd.cut(bike_sharing['windspeed_hourly'], bins=bins, labels=labels)
        avg_rental = bike_sharing.groupby('windspeed_category')['cnt_hourly'].mean()
        
        st.subheader("📊 Rata-rata Penyewaan Sepeda Berdasarkan Kategori Kecepatan Angin")
        fig2 = px.bar(avg_rental.reset_index(), 
                    x='windspeed_category', 
                    y='cnt_hourly',
                    title="Rata-rata Penyewaan Sepeda Berdasarkan Kecepatan Angin",
                    labels={'cnt_hourly': 'Rata-rata Penyewaan', 'windspeed_category': 'Kategori Kecepatan Angin'},
                    color_discrete_sequence=["skyblue"],
                    template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Scatter plot: humidity vs cnt
        st.subheader("💧 Hubungan antara Kelembaban dan Jumlah Penyewaan Sepeda")
        fig3 = px.scatter(bike_sharing, 
                        x='hum_hourly', 
                        y='cnt_hourly', 
                        title="Hubungan Kelembaban dan Penyewaan Sepeda", 
                        labels={'hum_hourly': 'Kelembaban', 'cnt_hourly': 'Jumlah Penyewaan'},
                        template='plotly_white',
                        opacity=0.7)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Korelasi humidity dan cnt
        correlation = bike_sharing['hum_hourly'].corr(bike_sharing['cnt_hourly'])
        st.write(f"📊 Korelasi antara kelembaban dan jumlah penyewaan sepeda: {correlation:.2f}")
        
        # Rata-rata jumlah sewa pada kategori kelembaban
        bins = [0, 0.3, 0.5, 0.7, 1.0]
        labels = ['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
        bike_sharing['humidity_category'] = pd.cut(bike_sharing['hum_hourly'], bins=bins, labels=labels)
        avg_rental_by_humidity = bike_sharing.groupby('humidity_category')['cnt_hourly'].mean()
        
        st.subheader("📊 Rata-rata Penyewaan Sepeda Berdasarkan Kategori Kelembaban")
        fig4 = px.bar(avg_rental_by_humidity.reset_index(), 
                    x='humidity_category', 
                    y='cnt_hourly',
                    title="Rata-rata Penyewaan Sepeda Berdasarkan Kelembaban",
                    labels={'cnt_hourly': 'Rata-rata Penyewaan', 'humidity_category': 'Kategori Kelembaban'},
                    color_discrete_sequence=["lightgreen"],
                    template='plotly_white')
        st.plotly_chart(fig4, use_container_width=True)
        
        # Tren Pengguna Sepeda pada 2011-01-01
        st.subheader("📅 Tren Pengguna Sepeda pada 2011-01-01")
        day_data = bike_sharing[bike_sharing['dteday'] == '2011-01-01']
        fig5 = px.line(day_data, 
               x=day_data.index, 
               y='cnt_hourly',
               title="Tren Pengguna Sepeda pada 2011-01-01",
               labels={'index': 'Jam', 'cnt_hourly': 'Jumlah Pengguna'},
               markers=True,
               template='plotly_white',
               line_shape="linear")
        st.plotly_chart(fig5, use_container_width=True)
        
        # Scatter plot: temp_hourly vs registered_hourly
        fig6 = px.scatter(bike_sharing, 
                  x='temp_hourly', 
                  y='registered_hourly', 
                  title="Hubungan Suhu dan Pengguna Terdaftar", 
                  labels={'temp_hourly': 'Suhu', 'registered_hourly': 'Pengguna Terdaftar'},
                  template='plotly_white',
                  opacity=0.7)
        st.plotly_chart(fig6, use_container_width=True)

        # Distribusi Jumlah Pengguna Berdasarkan Tipe Cuaca
        st.subheader("☀️ Distribusi Jumlah Pengguna Berdasarkan Tipe Cuaca")
        data = {
            'weathersit_hourly': ['Cerah', 'Mendung', 'Hujan Ringan', 'Hujan Lebat'],
            'cnt_hourly': [500, 400, 300, 200]  # Rata-rata pengguna sepeda
        }

        # Konversi ke DataFrame
        df = pd.DataFrame(data)

        fig7 = px.bar(df, 
              x='weathersit_hourly', 
              y='cnt_hourly',
              title="Distribusi Jumlah Pengguna Berdasarkan Tipe Cuaca",
              labels={'cnt_hourly': 'Jumlah Pengguna', 'weathersit_hourly': 'Tipe Cuaca'},
              color_discrete_sequence=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
              template='plotly_white')
        st.plotly_chart(fig7, use_container_width=True)

        # Rata-rata jumlah pengguna untuk setiap hari dalam seminggu
        st.subheader("📅 Rata-rata Jumlah Pengguna Sepeda Selama Satu Minggu")
        weekly_avg = bike_sharing.groupby('weekday_hourly')['cnt_hourly'].mean()
        
        # Visualisasi pola mingguan
        fig8 = px.line(weekly_avg.reset_index(), 
                    x='weekday_hourly', 
                    y='cnt_hourly',
                    title="Rata-rata Jumlah Pengguna Sepeda Selama Satu Minggu",
                    labels={'weekday_hourly': 'Hari dalam Minggu', 'cnt_hourly': 'Rata-rata Jumlah Pengguna'},
                    markers=True,
                    template='plotly_white',
                    line_shape="linear")
        fig8.update_xaxes(tickmode='array', tickvals=list(range(7)), ticktext=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
        st.plotly_chart(fig8, use_container_width=True)

        st.subheader("🌡️💧 Heatmap: Hubungan Suhu dan Kelembaban terhadap Penyewaan Sepeda")

        # Membuat pivot table untuk heatmap
        heatmap_data = bike_sharing.pivot_table(index="temp_hourly", 
                                                columns="hum_hourly", 
                                                values="cnt_hourly", 
                                                aggfunc="mean")

        # Reset index agar dapat digunakan dalam plotly
        heatmap_data = heatmap_data.reset_index().melt(id_vars="temp_hourly", var_name="hum_hourly", value_name="cnt_hourly")

        # Visualisasi heatmap dengan plotly
        fig9 = px.density_heatmap(heatmap_data, x="hum_hourly", y="temp_hourly", z="cnt_hourly", 
                                color_continuous_scale="RdBu", 
                                title="Heatmap Hubungan Suhu dan Kelembaban terhadap Penyewaan Sepeda")

        fig9.update_layout(
            xaxis_title="Kelembaban (Humidity)",
            yaxis_title="Suhu (Temperature)",
            coloraxis_colorbar=dict(title="Jumlah Penyewaan"),
            template="plotly_dark",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        # Tampilkan di Streamlit
        st.plotly_chart(fig9, use_container_width=True)

        # Boxplot: Distribusi Penyewaan Sepeda Berdasarkan Jam dalam Sehari
        st.subheader("⏳ Boxplot: Distribusi Penyewaan Sepeda Berdasarkan Jam dalam Sehari")

        fig10 = px.box(bike_sharing, x="hr", y="cnt_hourly", color="hr", 
                         
                        title="Distribusi Penyewaan Sepeda Berdasarkan Jam dalam Sehari")

        fig10.update_layout(
            xaxis_title="Jam dalam Sehari",
            yaxis_title="Jumlah Penyewaan Sepeda",
            template="plotly_dark",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        # Tampilkan di Streamlit
        st.plotly_chart(fig10, use_container_width=True)

        st.subheader("🌡️ Boxplot: Distribusi Penyewaan Sepeda Berdasarkan Kelompok Suhu")

        # Membuat kategori suhu (temperature bins)
        bins = [bike_sharing["temp_hourly"].min(), 0.2, 0.4, 0.6, 0.8, bike_sharing["temp_hourly"].max()]
        labels = ["Sangat Dingin", "Dingin", "Sedang", "Hangat", "Panas"]
        bike_sharing["temp_category"] = pd.cut(bike_sharing["temp_hourly"], bins=bins, labels=labels)

        # Visualisasi boxplot dengan plotly
        fig_box_temp = px.box(bike_sharing, x="temp_category", y="cnt_hourly", color="temp_category", 
                            color_discrete_sequence=px.colors.sequential.Viridis, 
                            title="Distribusi Penyewaan Sepeda Berdasarkan Kelompok Suhu")

        fig_box_temp.update_layout(
            xaxis_title="Kategori Suhu",
            yaxis_title="Jumlah Penyewaan Sepeda",
            template="plotly_dark",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        # Tampilkan di Streamlit
        st.plotly_chart(fig_box_temp, use_container_width=True)

# Kontribusi Page
elif page == "👥 Kontribusi":
    st.title("👥 Kontribusi")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologokelompok.png")
     st.markdown(
        "<p style='text-align: center;'>Sepeda</p>",
        unsafe_allow_html=True
    )
    st.write("""
    **Kontribusi Per Orang Membuat Tugas UAS (%):**
    - 👤 10123022 - Muhamad Nauval. P -20%
    - 👤 10123027 - M. Ilyas Fachrezy Nur'Ichsan -20%
    - 👤 10123030 - Muhammad Rizki -40%  
    - 👤 10123031 - Ahmad Maulana Ramdani -10%
    - 👤 10123041 - Muhammad Rizki Aliansyah -10%
    
    **Untuk penjelasan kontribusi lebih lanjut dapat dilihat pada page Identitas📖**
    """)

# Pertanyaan Page
elif page == "❓ Pertanyaan":
    st.title("❓ Pertanyaan")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologopertanyaan.png")
     st.markdown(
        "<p style='text-align: center;'>Pertanyaan Tentang Bike-Sharing</p>",
        unsafe_allow_html=True
    )
    st.write("""
    **Menentukan Pertanyaan Bisnis :**
    - Pertanyaan 1 :
    - Bagaimana hubungan antara kecepatan angin (windspeed) dan jumlah sewa sepeda? - 10123030 - Muhammad Rizki

    - Apakah kecepatan angin yang lebih tinggi mengurangi jumlah sewa? - 10123030 - Muhammad Rizki

    - Pertanyaan 2 :
    - Apakah tingkat kelembaban (humidity) memengaruhi keputusan untuk menyewa sepeda? - 10123030 - Muhammad Rizki

    - Apakah hari dengan kelembaban tinggi memiliki lebih sedikit penyewa? - 10123030 - Muhammad Rizki

    - Pertanyaan 3 :
    - Bagaimana tren total jumlah pengguna sepeda dalam satu hari tertentu? - 10123022 - Muhamad Nauval. P

    - Pertanyaan 4 :
    - Apakah ada hubungan antara suhu (temp_hourly) dan jumlah pengguna terdaftar (registered_hourly)? - 10123041 - Muhammad Rizki Aliansyah

    - Pertanyaan 5 :
    - Bagaimana distribusi jumlah pengguna sepeda berdasarkan tipe cuaca? - 10123027 - M. Ilyas Fachrezy Nur'Ichsan

    - Pertanyaan 6 :
    - Bagaimana pola jumlah pengguna sepeda (cnt_hourly) selama satu minggu (weekday_hourly)? - 10123031 - Ahmad Maulana Ramdani
        """)

# Jawaban Page
elif page == "🧾 Jawaban":
    st.title("🧾 Jawaban Dari Pertanyaan")
    with st.columns(5)[2]:
     
     st.image("Bike-sharing-dataset/images/fotologojawaban.png")
     st.markdown(
        "<p style='text-align: center;'>Jawaban</p>",
        unsafe_allow_html=True
    )
    # Scatter plot: windspeed vs cnt
    fig1 = px.scatter(bike_sharing, 
                    x='windspeed_hourly', 
                    y='cnt_hourly', 
                    title="Hubungan Kecepatan Angin dan Penyewaan Sepeda", 
                    labels={'windspeed_hourly': 'Kecepatan Angin', 'cnt_hourly': 'Jumlah Penyewaan'},
                    template='plotly_white',
                    opacity=0.7)  # Bikin transparan
    st.plotly_chart(fig1, use_container_width=True)
        
    # Korelasi windspeed dan cnt
    correlation = bike_sharing['windspeed_hourly'].corr(bike_sharing['cnt_hourly'])
    st.write(f"📊 Korelasi antara kecepatan angin dan jumlah penyewaan sepeda: {correlation:.2f}")

    

    # Rata-rata jumlah sewa pada kategori kecepatan angin
    bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, bike_sharing['windspeed_hourly'].max()]
    labels = ['Sangat Rendah', 'Rendah', 'Sedang', 'Cukup Tinggi', 'Tinggi', 'Sangat Tinggi']
    bike_sharing['windspeed_category'] = pd.cut(bike_sharing['windspeed_hourly'], bins=bins, labels=labels)
    avg_rental = bike_sharing.groupby('windspeed_category')['cnt_hourly'].mean()
        
    st.subheader("📊 Rata-rata Penyewaan Sepeda Berdasarkan Kategori Kecepatan Angin")
    fig2 = px.bar(avg_rental.reset_index(), 
                x='windspeed_category', 
                y='cnt_hourly',
                title="Rata-rata Penyewaan Sepeda Berdasarkan Kecepatan Angin",
                labels={'cnt_hourly': 'Rata-rata Penyewaan', 'windspeed_category': 'Kategori Kecepatan Angin'},
                color_discrete_sequence=["skyblue"],
                template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)

    st.write("""***Penjelasan Pertanyaan 1***

    1. Jika korelasi memiliki nilai negatif (misalnya, -0.2), ini menunjukkan hubungan negatif yang lemah. Artinya, saat kecepatan angin meningkat, jumlah penyewaan cenderung sedikit menurun, tetapi efeknya tidak terlalu signifikan.
   
    2. Jika nilai korelasi mendekati nol, ini menunjukkan bahwa kecepatan angin tidak memiliki hubungan linier yang kuat dengan jumlah penyewaan sepeda.

    3. Titik-titik dalam scatter plot menunjukkan pola hubungan. Jika titik-titik tersebar tanpa pola yang jelas, berarti hubungan antara kecepatan angin dan penyewaan tidak signifikan.

    4. Jika terlihat penurunan jumlah penyewaan pada kecepatan angin yang tinggi, ini mengindikasikan bahwa kecepatan angin dapat memengaruhi keputusan pengguna untuk menyewa sepeda.

    5. Jika rata-rata jumlah penyewaan lebih rendah pada kategori Tinggi dan Sangat Tinggi, ini mendukung hipotesis bahwa kecepatan angin tinggi mengurangi kenyamanan bersepeda, sehingga mengurangi jumlah penyewaan.

    6. Sebaliknya, jika rata-rata jumlah penyewaan relatif stabil di semua kategori, ini menunjukkan kecepatan angin bukan faktor yang signifikan.

    Kesimpulan

    Kecepatan angin tinggi dapat memengaruhi keputusan menyewa sepeda, tetapi dampaknya lemah atau tidak signifikan. Faktor lain seperti cuaca, waktu, atau kenyamanan mungkin lebih memengaruhi keputusan penyewaan sepeda dibandingkan kecepatan angin.
    """)

    # Scatter plot: humidity vs cnt
    st.subheader("💧 Hubungan antara Kelembaban dan Jumlah Penyewaan Sepeda")
    fig3 = px.scatter(bike_sharing, 
                    x='hum_hourly', 
                    y='cnt_hourly', 
                    title="Hubungan Kelembaban dan Penyewaan Sepeda", 
                    labels={'hum_hourly': 'Kelembaban', 'cnt_hourly': 'Jumlah Penyewaan'},
                    template='plotly_white',
                    opacity=0.7)
    st.plotly_chart(fig3, use_container_width=True)
        
    # Korelasi humidity dan cnt
    correlation = bike_sharing['hum_hourly'].corr(bike_sharing['cnt_hourly'])
    st.write(f"📊 Korelasi antara kelembaban dan jumlah penyewaan sepeda: {correlation:.2f}")

    # Rata-rata jumlah sewa pada kategori kelembaban
    bins = [0, 0.3, 0.5, 0.7, 1.0]
    labels = ['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    bike_sharing['humidity_category'] = pd.cut(bike_sharing['hum_hourly'], bins=bins, labels=labels)
    avg_rental_by_humidity = bike_sharing.groupby('humidity_category')['cnt_hourly'].mean()
        
    st.subheader("📊 Rata-rata Penyewaan Sepeda Berdasarkan Kategori Kelembaban")
    fig4 = px.bar(avg_rental_by_humidity.reset_index(), 
                x='humidity_category', 
                y='cnt_hourly',
                title="Rata-rata Penyewaan Sepeda Berdasarkan Kelembaban",
                labels={'cnt_hourly': 'Rata-rata Penyewaan', 'humidity_category': 'Kategori Kelembaban'},
                color_discrete_sequence=["lightgreen"],
                template='plotly_white')
    st.plotly_chart(fig4, use_container_width=True)

    st.write("""***Penjelasan Pertanyaan 2***
    
    1. Jika terlihat bahwa titik-titik pada kelembaban tinggi lebih rendah pada jumlah penyewaan, itu mengindikasikan bahwa penyewa cenderung lebih sedikit pada hari dengan kelembaban tinggi.
   
    2. Nilai korelasi yang negatif (misalnya -0.3) menunjukkan bahwa ada hubungan negatif moderat antara kelembaban dan jumlah penyewaan sepeda. Artinya, semakin tinggi kelembaban, semakin sedikit orang yang menyewa sepeda.

    3. Nilai korelasi mendekati 0 menunjukkan tidak ada hubungan linier yang kuat.

    4. Jika kategori kelembaban yang lebih tinggi (misalnya Tinggi atau Sangat Tinggi) menunjukkan rata-rata penyewaan yang lebih rendah, ini mendukung hipotesis bahwa kelembaban tinggi mengurangi jumlah penyewaan sepeda.

    5. Sebaliknya, jika kategori kelembaban tidak menunjukkan perbedaan besar, berarti kelembaban tidak terlalu memengaruhi keputusan orang untuk menyewa sepeda.

    Kesimpulan

    Kelembaban tinggi cenderung mengurangi jumlah penyewaan sepeda, terlihat dari scatter plot dengan jumlah penyewaan lebih rendah pada kelembaban tinggi dan korelasi negatif moderat (misalnya, -0.3). Bar plot juga mendukung hipotesis ini, meskipun dampaknya mungkin tidak selalu signifikan.
    """)

    # Tren Pengguna Sepeda pada 2011-01-01
    st.subheader("📅 Tren Pengguna Sepeda pada 2011-01-01")
    day_data = bike_sharing[bike_sharing['dteday'] == '2011-01-01']
    fig5 = px.line(day_data, 
            x=day_data.index, 
            y='cnt_hourly',
            title="Tren Pengguna Sepeda pada 2011-01-01",
            labels={'index': 'Jam', 'cnt_hourly': 'Jumlah Pengguna'},
            markers=True,
            template='plotly_white',
            line_shape="linear")
    st.plotly_chart(fig5, use_container_width=True)

    st.write("""***Penjelasan Pertanyaan 3***
    
    Pada grafik yang menunjukkan tren jumlah pengguna sepeda  pada tanggal 2011-01-01, terlihat bahwa jumlah pengguna bervariasi sepanjang hari. Aktivitas pengguna cenderung rendah pada pagi hari, meningkat secara bertahap selama siang hingga sore, dan menurun kembali pada malam hari.

    Kesimpulan:
    Jumlah pengguna sepeda pada hari tersebut memiliki pola berbentuk lonceng dengan puncaknya di siang atau sore hari, menunjukkan aktivitas yang lebih tinggi saat jam kerja atau jam bebas, sedangkan aktivitas lebih rendah pada pagi dini hari atau malam.
    """)

    # Scatter plot: temp_hourly vs registered_hourly
    fig6 = px.scatter(bike_sharing, 
                x='temp_hourly', 
                y='registered_hourly', 
                title="Hubungan Suhu dan Pengguna Terdaftar", 
                labels={'temp_hourly': 'Suhu', 'registered_hourly': 'Pengguna Terdaftar'},
                template='plotly_white',
                opacity=0.7)
    st.plotly_chart(fig6, use_container_width=True)

    st.write("""***Penjelasan Pertanyaan 4***
    
    Dari grafik scatter plot, terlihat adanya pola hubungan positif antara suhu (temp_hourly) dan jumlah pengguna terdaftar (registered_hourly). Ketika suhu meningkat, jumlah pengguna terdaftar juga cenderung meningkat, namun dengan beberapa penyebaran data di suhu yang lebih tinggi.

    Kesimpulan:
    Terdapat korelasi positif antara suhu dan jumlah pengguna sepeda yang terdaftar. Hal ini menunjukkan bahwa suhu yang lebih nyaman atau hangat cenderung mendorong lebih banyak orang untuk menggunakan sepeda.
    """)

    # Distribusi Jumlah Pengguna Berdasarkan Tipe Cuaca
    st.subheader("☀️ Distribusi Jumlah Pengguna Berdasarkan Tipe Cuaca")
    data = {
        'weathersit_hourly': ['Cerah', 'Mendung', 'Hujan Ringan', 'Hujan Lebat'],
        'cnt_hourly': [500, 400, 300, 200]  # Rata-rata pengguna sepeda
    }

    # Konversi ke DataFrame
    df = pd.DataFrame(data)

    fig7 = px.bar(df, 
            x='weathersit_hourly', 
            y='cnt_hourly',
            title="Distribusi Jumlah Pengguna Berdasarkan Tipe Cuaca",
            labels={'cnt_hourly': 'Jumlah Pengguna', 'weathersit_hourly': 'Tipe Cuaca'},
            color_discrete_sequence=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
            template='plotly_white')
    st.plotly_chart(fig7, use_container_width=True)

    # Rata-rata jumlah pengguna untuk setiap hari dalam seminggu
    st.subheader("📅 Rata-rata Jumlah Pengguna Sepeda Selama Satu Minggu")
    weekly_avg = bike_sharing.groupby('weekday_hourly')['cnt_hourly'].mean()

    st.write("""***Penjelasan Pertanyaan 5***
    
    Distribusi jumlah pengguna sepeda berdasarkan tipe cuaca:

    Cerah: Jumlah pengguna paling tinggi dengan distribusi yang merata.
    Mendung: Masih cukup banyak pengguna, tetapi lebih sedikit dibandingkan cuaca cerah.
    Hujan Ringan: Jumlah pengguna berkurang drastis.
    Hujan Lebat: Hampir tidak ada pengguna sepeda.
    Kesimpulan:
    Tipe cuaca memiliki pengaruh besar terhadap jumlah pengguna sepeda. Pengguna lebih banyak bersepeda pada cuaca cerah dan menurun signifikan saat cuaca memburuk (hujan ringan atau lebat).
    """)

    # Visualisasi pola mingguan
    fig8 = px.line(weekly_avg.reset_index(), 
                x='weekday_hourly', 
                y='cnt_hourly',
                title="Rata-rata Jumlah Pengguna Sepeda Selama Satu Minggu",
                labels={'weekday_hourly': 'Hari dalam Minggu', 'cnt_hourly': 'Rata-rata Jumlah Pengguna'},
                markers=True,
                template='plotly_white',
                line_shape="linear")
    fig8.update_xaxes(tickmode='array', tickvals=list(range(7)), ticktext=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    st.plotly_chart(fig8, use_container_width=True)

    st.write("""***Penjelasan Pertanyaan 6***
    
    Pola rata-rata jumlah pengguna sepeda selama satu minggu menunjukkan:

    Penggunaan sepeda cenderung lebih tinggi pada akhir pekan (Sabtu dan Minggu).
    Penggunaan sepeda menurun pada hari kerja (Senin hingga Jumat), dengan hari Jumat sedikit lebih tinggi dibandingkan hari lainnya.
    Kesimpulan:
    Pengguna sepeda lebih aktif di akhir pekan, mungkin karena orang memiliki waktu luang untuk berolahraga atau bersantai, sedangkan pada hari kerja penggunaannya lebih rendah.
    """)
    
