import pandas as pd
import zipfile
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# Initialize Files
hour_file = 'bike-sharing-dataset/hour.csv'
day_file = 'bike-sharing-dataset/day.csv'

# Sidebar for selecting the year and month
with st.sidebar:
    # Select a year using selectbox
    year = st.selectbox(
        label='Pilih Tahun',
        options=range(1, 4),
        format_func=lambda x: ['2011', '2012', 'All'][x - 1]
    )
    # Select a month using selectbox
    month = st.selectbox(
        label='Pilih Bulan',
        options=range(1, 14),  # 1-12 for months, 13 for "All"
        format_func=lambda x: ['January', 'February', 'March', 'April', 'May', 'June',
                                'July', 'August', 'September', 'October', 'November', 'December', 'All'][x - 1]
    )

# Main title for the dashboard
st.header('[Bike Sharing Dataset] Dashboard')
st.subheader("Pola Distribusi Penyewaan Berdasarkan Jam")

hour_df = pd.read_csv(hour_file)
day_df = pd.read_csv(day_file)

# Filter the DataFrame based on the selected month and year
hour_filtered_df = hour_df.copy()
day_filtered_df = day_df.copy()
if month != 13:  # Apply month filter if "All" is not selected
    hour_filtered_df = hour_filtered_df[hour_filtered_df['mnth'] == month]
    day_filtered_df = day_filtered_df[day_filtered_df['mnth'] == month]
if year != 3:  # Apply year filter if "All" is not selected
    hour_filtered_df = hour_filtered_df[hour_filtered_df['yr'] == (year - 1)]
    day_filtered_df = day_filtered_df[day_filtered_df['yr'] == (year - 1)]

# Use columns to create a layout for the first set of visualizations
col1, col2 = st.columns(2)

# Create visualizations for each column
with col1:
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    sns.barplot(x='hr', y='cnt', data=hour_filtered_df[hour_filtered_df['holiday'] == 0], ax=ax1, palette="crest")
    ax1.set_title(f'Distribusi Penyewaan Sepeda Setiap Jam (Hari Kerja) - Bulan {month}')
    ax1.set_xlabel('Jam')
    ax1.set_ylabel('Jumlah Penyewaan')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    sns.barplot(x='hr', y='cnt', data=hour_filtered_df[hour_filtered_df['holiday'] == 1], ax=ax2, palette="crest")
    ax2.set_title(f'Distribusi Penyewaan Sepeda Setiap Jam (Hari Libur) - Bulan {month}')
    ax2.set_xlabel('Jam')
    ax2.set_ylabel('Jumlah Penyewaan')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig2)

# Create another row of columns for the weather condition visualizations
st.subheader("Hubungan Antar Parameter Terhadap Jumlah Penyewaan Sepeda")
col3, col4 = st.columns(2)
        # Mapping weather conditions
weather_day = {1: 'Cerah', 2: 'Kabut', 3: 'Hujan Ringan'}
day_filtered_df['Kondisi Cuaca Day'] = day_filtered_df['weathersit'].map(weather_day)

weather_hour = {1: 'Cerah', 2: 'Kabut', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
hour_filtered_df['Kondisi Cuaca Hour'] = hour_filtered_df['weathersit'].map(weather_hour)

# Visualize the impact of daily weather conditions
with col3:
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    sns.barplot(x='weathersit', y='cnt', hue='Kondisi Cuaca Day', data=day_filtered_df, ax=ax3, palette="crest")
    ax3.set_title('Pengaruh Suhu Harian terhadap Jumlah Penyewaan Sepeda')
    ax3.set_xlabel('Cuaca Harian')
    ax3.set_ylabel('Jumlah Penyewaan')
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig3)

# Visualize the impact of hourly weather conditions
with col4:
    fig4, ax4 = plt.subplots(figsize=(7, 5))
    sns.barplot(x='weathersit', y='cnt', hue='Kondisi Cuaca Hour', data=hour_filtered_df, ax=ax4, palette="crest")
    ax4.set_title('Pengaruh Suhu per Jam terhadap Jumlah Penyewaan Sepeda')
    ax4.set_xlabel('Cuaca per Jam')
    ax4.set_ylabel('Jumlah Penyewaan')
    ax4.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig4)


# Create the season
season_labels = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.boxplot(x='season', y='cnt', hue='Kondisi Cuaca Day', data=day_filtered_df, ax=ax5)
ax5.set_title('Pengaruh Musim dan Cuaca terhadap Jumlah Penyewaan Sepeda Harian')
ax5.set_xlabel('Musim')
ax5.set_ylabel('Jumlah Penyewaan')
# Set custom x-tick labels using the season_labels dictionary
ax5.set_xticklabels([season_labels[int(x.get_text())] for x in ax5.get_xticklabels()])

st.pyplot(fig5)


# Buat peta cuaca untuk legend yang deskriptif
weather_mapping = {1: 'Cerah', 2: 'Kabut', 3: 'Hujan Ringan'}

# Menambahkan kolom baru 'weather_desc' pada dataframe day_df
day_filtered_df['Kondisi Cuaca'] = day_filtered_df['weathersit'].map(weather_mapping)
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Scatter plot untuk temp
sns.scatterplot(x='temp', y='cnt', hue='Kondisi Cuaca', data=day_filtered_df, ax=axes[0, 0])
axes[0, 0].set_title('Hubungan Antara Suhu dengan Jumlah Penyewaan Sepeda Harian')
axes[0, 0].set_xlabel('Suhu (Temp)')
axes[0, 0].set_ylabel('Jumlah Penyewaan')
# Scatter plot untuk atemp
sns.scatterplot(x='atemp', y='cnt', hue='Kondisi Cuaca', data=day_filtered_df, ax=axes[0, 1])
axes[0, 1].set_title('Hubungan Antara Suhu yang Dirasakan dengan Jumlah Penyewaan Sepeda Harian')
axes[0, 1].set_xlabel('Suhu yang Dirasakan (Atemp)')
axes[0, 1].set_ylabel('Jumlah Penyewaan')
# Scatter plot untuk windspeed
sns.scatterplot(x='windspeed', y='cnt', hue='Kondisi Cuaca', data=day_filtered_df, ax=axes[1, 0])
axes[1, 0].set_title('Hubungan Antara Kecepatan Angin dengan Jumlah Penyewaan Sepeda Harian')
axes[1, 0].set_xlabel('Kecepatan Angin (Windspeed)')
axes[1, 0].set_ylabel('Jumlah Penyewaan')
# Scatter plot untuk hum
sns.scatterplot(x='hum', y='cnt', hue='Kondisi Cuaca', data=day_filtered_df, ax=axes[1, 1])
axes[1, 1].set_title('Hubungan Antara Kelembapan dengan Jumlah Penyewaan Sepeda Harian')
axes[1, 1].set_xlabel('Kelembapan (Hum)')
axes[1, 1].set_ylabel('Jumlah Penyewaan')
# Adjust layout to prevent overlapping elements
plt.tight_layout()
# Display the figure in Streamlit
st.pyplot(fig)

st.subheader("Statistik Bulanan")
st.dataframe(hour_filtered_df.describe())
