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

st.header("Ringkasan Data")
st.write(data.head())

st.header("Tren PM2.5 dari Waktu ke Waktu")

data['datetime'] = pd.to_datetime(data['datetime'])

daily_data = data[['datetime', 'PM2.5']].set_index('datetime').resample('D').mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(daily_data['datetime'], daily_data['PM2.5'], color='blue', linewidth=1)
ax1.set_title("Tren PM2.5 Harian (Resampled)")
ax1.set_xlabel("Waktu")
ax1.set_ylabel("PM2.5")
st.pyplot(fig1)

st.header("Korelasi PM2.5 dengan Variabel Meteorologi")

data.reset_index(drop=True, inplace=True)
cols_meteorologi = ['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
corr_matrix = data[cols_meteorologi].corr()

fig2, ax2 = plt.subplots(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='YlGnBu', ax=ax2)
ax2.set_title("Korelasi antara PM2.5 dan Variabel Meteorologi")
st.pyplot(fig2)

st.sidebar.header("Filter Data")
years = data['year'].unique()
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(years))
filtered_data = data[data['year'] == selected_year]

st.subheader(f"Data Tahun {selected_year}")
st.write(filtered_data.head())
