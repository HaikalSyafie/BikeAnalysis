import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('hour.csv')

# Map years for clarity
df['yr'] = df['yr'].replace({0: 2011, 1: 2012})

# Map months to names
month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
df['mnth'] = df['mnth'].map(month_names)

# Map weathersit to shorter descriptive labels
weather_labels = {
    1: 'Clear/Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Snow'
}
df['weathersit'] = df['weathersit'].map(weather_labels)

# Streamlit dashboard
st.title("Dashboard Penyewaan Sepeda")

st.sidebar.header("Filter Data")
year_filter = st.sidebar.selectbox("Pilih Tahun:", options=[2011, 2012, "All"])
month_filter = st.sidebar.selectbox("Pilih Bulan:", options=list(df['mnth'].unique()) + ["All"])

# Filtering the data based on user selections
if year_filter == "All" and month_filter == "All":
    filtered_df = df
elif year_filter == "All":
    filtered_df = df[df['mnth'] == month_filter]
elif month_filter == "All":
    filtered_df = df[df['yr'] == year_filter]
else:
    filtered_df = df[(df['yr'] == year_filter) & (df['mnth'] == month_filter)]

st.subheader("Jumlah penyewaan berdasarkan hari")
st.write("Diagram ini menunjukkan hubungan antara hari kerja, hari libur dengan jumlah penyewaan sepeda.(pencet tombol expand untuk lebih jelas)")

day_vars = ['hr', 'holiday', 'workingday']
n_day_vars = len(day_vars)  
fig, axes = plt.subplots(nrows=(n_day_vars + 1) // 2, ncols=2, figsize=(18, 13)) 
axes = axes.flatten()

for i, var in enumerate(day_vars):
    total_cnt = filtered_df.groupby(var)['cnt'].sum().reset_index()
    sns.barplot(data=total_cnt, x=var, y='cnt', palette='Blues_d', ci=None, ax=axes[i])
    axes[i].set_xlabel(var.capitalize(), fontsize=14)
    axes[i].set_ylabel('Total Penyewaan', fontsize=14)
    axes[i].set_title(f"Total Penyewaan berdasarkan {var.capitalize()}", fontsize=16)  # Set title for each plot

for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
st.pyplot(fig)

st.subheader("Hubungan parameter Cuaca dengan Jumlah Penyewaan")
st.write("Di sini kita melihat bagaimana kondisi cuaca mempengaruhi jumlah penyewaan sepeda.(pencet tombol expand untuk lebih jelas)")

numerical_features = ['temp', 'atemp', 'hum', 'windspeed', 'weathersit']
n_numerical_features = len(numerical_features)  
fig, axes = plt.subplots(nrows=(n_numerical_features + 1) // 2, ncols=2, figsize=(18, 13))  
axes = axes.flatten()

for i, feature in enumerate(numerical_features):
    if feature in filtered_df.columns and 'cnt' in filtered_df.columns:  # Ensure columns exist
        sns.scatterplot(data=filtered_df, x=feature, y='cnt', color='blue', ax=axes[i])
        axes[i].set_xlabel(feature.capitalize(), fontsize=14)
        axes[i].set_ylabel("Jumlah Penyewaan (cnt)", fontsize=14)
        axes[i].set_title(f"Hubungan {feature.capitalize()} dengan Jumlah Penyewaan", fontsize=16)  # Set title for each plot

for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
st.pyplot(fig)

st.subheader("Statistik Data")
st.write(df.describe())

# Custom CSS styling
st.markdown("""
<style>
body {
    background-color: #f0f2f5;
    font-family: Arial, sans-serif;
}
h1 {
    color: #4A4A4A;
    font-size: 32px;  
}
h2 {
    color: #4A4A4A;
    font-size: 28px;  
}
h3 {
    color: #4A4A4A;
    font-size: 24px;  
}
p {
    font-size: 18px;  
}
</style>
""", unsafe_allow_html=True)
