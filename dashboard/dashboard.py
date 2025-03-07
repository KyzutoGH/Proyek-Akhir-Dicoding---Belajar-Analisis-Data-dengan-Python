import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    
    numeric_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if 'datetime' not in df.columns:
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        df = df.sort_values('datetime')
    return df

data = load_data('dashboard/main_data.csv')

st.title("Dashboard Analisis Kualitas Udara")

st.sidebar.header("Filter Data")

years = sorted(data['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun", years)

filtered_data = data[data['year'] == selected_year]

min_pm25 = float(filtered_data['PM2.5'].min())
max_pm25 = float(filtered_data['PM2.5'].max())
selected_pm25 = st.sidebar.slider("Pilih Rentang PM2.5", min_pm25, max_pm25, (min_pm25, max_pm25))

filtered_data = filtered_data[
    (filtered_data['PM2.5'] >= selected_pm25[0]) & 
    (filtered_data['PM2.5'] <= selected_pm25[1])
]

st.header(f"Ringkasan Data Tahun {selected_year}")
st.write(filtered_data.head())

st.header("Tren PM2.5 dari Waktu ke Waktu")

filtered_data['datetime'] = pd.to_datetime(filtered_data['datetime'])
filtered_data = filtered_data.sort_values('datetime')

daily_data = filtered_data[['datetime', 'PM2.5']].set_index('datetime').resample('D').mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(daily_data['datetime'], daily_data['PM2.5'], color='blue', linewidth=1)
ax1.set_title(f"Tren PM2.5 Harian Tahun {selected_year}")
ax1.set_xlabel("Waktu")
ax1.set_ylabel("PM2.5")
st.pyplot(fig1)

st.header("Korelasi PM2.5 dengan Variabel Meteorologi")

filtered_data.reset_index(drop=True, inplace=True)
cols_meteorologi = ['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
corr_matrix = filtered_data[cols_meteorologi].corr()

fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='YlGnBu', ax=ax2)
ax2.set_title(f"Korelasi antara PM2.5 dan Variabel Meteorologi Tahun {selected_year}")
st.pyplot(fig2)
