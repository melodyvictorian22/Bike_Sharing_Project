# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from millify import millify

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# mengubah tipe data menjadi datetime pada day
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# mengubah tipe data menjadi datetime pada hour
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# menambahkan nama hari pada dataframe
day_df['day_of_week'] = pd.to_datetime(day_df['dteday']).dt.day_name()

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar :
    # Menambahkan logo perusahaan
    st.image("bicycle.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

st.header('Bike Sharing Dashboard :bike:')

col1, col2, col3 = st.columns(3)
 
with col1:
    jumlah_sepeda = main_df["cnt"].sum()
    st.metric("Jumlah Penyewa Sepeda", millify(jumlah_sepeda))
 
with col2:
    non_member = main_df["casual"].sum()
    st.metric("Penyewa Non Member", millify(non_member))
    
with col3:
    member = main_df["registered"].sum()
    st.metric("Penyewa Member", millify(member))

# Peminjaman sepeda berdasarkan musim
st.subheader('Jumlah Peminjaman Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(16, 8))
season_df = main_df.groupby(by="season").cnt.mean()
season = ['Spring', 'Summer', 'Fall', 'Winter']
ax.bar(season, season_df)
ax.set_xlabel('Musim', fontsize = 30)
ax.set_ylabel('Rata-rata sewa', fontsize = 30)
ax.set_title('Peminjaman Sepeda Terhadap Musim', fontsize=45)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30) 
st.pyplot(fig)

# peminjaman sepeda berdasarkan cuaca
st.subheader('Jumlah Peminjaman Sepeda Berdasarkan Cuaca')
fig, ax = plt.subplots(figsize=(16, 8))
weather_df = hour_df.groupby(by="weathersit").cnt.mean()
weather = ['Clear', 'Mist', 'Light', 'Heavy']
ax.bar(weather, weather_df)
ax.set_xlabel('Cuaca', fontsize=30)
ax.set_ylabel('Rata-rata sewa', fontsize=30)
ax.set_title('Peminjaman Sepeda Terhadap Cuaca', fontsize=45)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30) 
st.pyplot(fig)

st.subheader('Pola Peminjaman Sepeda Berdasarkan Waktu')

# Pola peminjaman sepeda terhadap hari
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="day_of_week", y="cnt", data=main_df)
ax.set_title("Pola Peminjaman Sepeda Terhadap Hari", fontsize=45)
ax.set_xlabel("Hari", fontsize=30)
ax.set_ylabel("Jumlah Sewa", fontsize=30)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=30) 

st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
# Pola peminjaman sepeda terhadap bulan
sns.lineplot(x="mnth", y="cnt", data=main_df, ax=ax[0])
ax[0].set_title("Pola Peminjaman Sepeda Terhadap Bulan", fontsize=45)
ax[0].set_xlabel("Bulan", fontsize=30)
ax[0].set_ylabel("Jumlah Sewa", fontsize=30)
ax[0].tick_params(axis='x', labelsize=35)
ax[0].tick_params(axis='y', labelsize=30)


# Pola peminjaman sepeda terhadap waktu
sns.lineplot(x="hr", y="cnt", data=hour_df, ax=ax[1])
ax[1].set_title("Pola Peminjaman Sepeda Terhadap Waktu", fontsize=45)
ax[1].set_xlabel("Waktu", fontsize=30)
ax[1].set_ylabel("Jumlah Sewa", fontsize=30)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].tick_params(axis='y', labelsize=30)

st.pyplot(fig)