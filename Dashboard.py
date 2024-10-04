import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('hour.csv')


df['yr'] = df['yr'].replace({0: 2011, 1: 2012})


st.title("Dashboard Penyewaan Sepeda")



st.sidebar.header("Filter Data")
year_filter = st.sidebar.selectbox("Pilih Tahun:", options=[2011, 2012, "All"])
month_filter = st.sidebar.selectbox("Pilih Bulan:", options=list(df['mnth'].unique()) + ["All"])


if year_filter == "All" and month_filter == "All":
    filtered_df = df
elif year_filter == "All":
    filtered_df = df[df['mnth'] == month_filter]
elif month_filter == "All":
    filtered_df = df[df['yr'] == year_filter]
else:
    filtered_df = df[(df['yr'] == year_filter) & (df['mnth'] == month_filter)]


st.subheader("Jumlah penyewaan berdasarkan hari ")
st.write("Diagram ini menunjukkan hubungan antara hari kerja, hari libur dengan jumlah penyewaan sepeda.(pencet tombol expand untuk lebih jelas)")

day_vars = ['hr', 'holiday', 'workingday']
n_day_vars = len(day_vars)  
fig, axes = plt.subplots(nrows=(n_day_vars + 1) // 2, ncols=2, figsize=(18, 13)) 


axes = axes.flatten()


for i, var in enumerate(day_vars):
    # Menghitung total cnt per kategori
    total_cnt = filtered_df.groupby(var)['cnt'].sum().reset_index()
    sns.barplot(data=total_cnt, x=var, y='cnt', palette='Blues_d', ci=None, ax=axes[i])
    axes[i].set_title(f'Total Penyewaan Berdasarkan {var.capitalize()}', fontsize=16)
    axes[i].set_xlabel(var.capitalize(), fontsize=14)
    axes[i].set_ylabel('Total Penyewaan', fontsize=14)


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
        axes[i].set_title(f"Jumlah Penyewaan vs {feature.capitalize()}", fontsize=16)
        axes[i].set_xlabel(feature.capitalize(), fontsize=14)
        axes[i].set_ylabel("Jumlah Penyewaan (cnt)", fontsize=14)


for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])


plt.tight_layout()
st.pyplot(fig)


st.subheader("Statistik Data")
st.write(df.describe())


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
