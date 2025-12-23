import streamlit as st
import pandas as pd
from PIL import Image
import joblib  # <--- WAJIB IMPORT INI UNTUK BACA MODEL

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Dashboard PT. LDN", page_icon="🛡️", layout="wide")

# --- LOAD MODEL MACHINE LEARNING ---
try:
    model_estimasi = joblib.load('model_estimasi.sav')
except FileNotFoundError:
    st.error("File 'model_estimasi.sav' tidak ditemukan. Jalankan latih_model.py dulu!")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("Navigasi")
try:
    logo = Image.open("20251206_1936_image.jpg")
    st.sidebar.image(logo, use_container_width=True)
except:
    pass

menu = st.sidebar.radio("Pilih Menu:", ["Laporan Penjualan", "🤖 Prediksi Waktu Pengerjaan"])

# ==========================================
# HALAMAN 1: LAPORAN PENJUALAN (YANG TADI)
# ==========================================
if menu == "Laporan Penjualan":
    st.title("📊 Laporan Penjualan - PT. Loyalita Dharma Nusantara")
    st.markdown("---")
    
    # Data Dummy SPH
    df = pd.DataFrame({
        'Nama Barang': ['Wearpack Pertamina', 'Wearpack Orange', 'Wearpack Driver', 'Jas Lab', 'Wearpack Anti Bara'],
        'Harga Satuan': [800000, 700000, 700000, 150000, 550000],
        'Terjual': [50, 35, 20, 100, 45]
    })
    df['Total Omzet'] = df['Harga Satuan'] * df['Terjual']
    
    # Metrik Sederhana
    col1, col2 = st.columns(2)
    col1.metric("Total Omzet", f"Rp {df['Total Omzet'].sum():,.0f}")
    col2.metric("Total Unit", f"{df['Terjual'].sum()} Pcs")
    
    st.bar_chart(df.set_index('Nama Barang')['Total Omzet'])

# ==========================================
# HALAMAN 2: PREDIKSI AI (INI YANG BARU) 🧠
# ==========================================
elif menu == "🤖 Prediksi Waktu Pengerjaan":
    st.title("🤖 Simulasi Estimasi Waktu Produksi")
    st.info("Fitur ini menggunakan Machine Learning untuk memprediksi lama pengerjaan berdasarkan kuantitas pesanan.")
    
    st.markdown("---")
    
    # Input User
    col_input, col_hasil = st.columns(2)
    
    with col_input:
        st.subheader("Masukkan Data Pesanan")
        qty_input = st.number_input("Jumlah Pesanan (Pcs)", min_value=1, value=100)
        
        # Tombol Prediksi
        if st.button("Hitung Estimasi Waktu 🚀"):
            # Lakukan Prediksi menggunakan Model yang sudah di-load
            prediksi_hari = model_estimasi.predict([[qty_input]])[0]
            
            # Tampilkan Hasil di kolom sebelah
            with col_hasil:
                st.success("Hasil Prediksi:")
                st.metric("Estimasi Waktu", f"{prediksi_hari:.1f} Hari Kerja")
                
                if prediksi_hari > 30:
                    st.warning("⚠️ Pesanan jumlah besar membutuhkan waktu lebih dari 1 bulan.")
                else:
                    st.success("✅ Pesanan dapat diselesaikan kurang dari 1 bulan.")