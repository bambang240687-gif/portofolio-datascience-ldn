import streamlit as st
import pdfplumber
import pandas as pd
import re
from io import BytesIO

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Ekstraktor Invoice Otomatis", page_icon="📄")

st.title("📄 Aplikasi OCR Invoice & SPH")
st.markdown("Upload file PDF Invoice/SPH Anda, dan biarkan AI mengekstrak data pentingnya ke Excel.")

# --- Upload File ---
uploaded_files = st.file_uploader("Upload File PDF (Bisa Banyak Sekaligus)", type="pdf", accept_multiple_files=True)

# Tombol Eksekusi
if st.button("Ekstrak Data 🚀") and uploaded_files:
    
    data_hasil = [] # List untuk menampung hasil semua file
    
    # Progress Bar (Biar terlihat canggih)
    progress_bar = st.progress(0)
    
    for i, file_pdf in enumerate(uploaded_files):
        with pdfplumber.open(file_pdf) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            # --- LOGIKA EKSTRAKSI (REGEX) ---
            # Di sini kita menyuruh Python mencari pola teks tertentu
            
            # 1. Cari Nomor Invoice / Surat
            # Pola: Mencari kata setelah "No." atau "Nomor"
            no_surat = re.search(r'(No\.|Nomor)\s*[:.]?\s*([A-Za-z0-9/]+)', text)
            no_surat = no_surat.group(2) if no_surat else "Tidak Ditemukan"
            
            # 2. Cari Tanggal
            # Pola: Mencari format tanggal umum (misal: 21/11/2025 atau 4 November 2025)
            tanggal = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4}|\d{1,2}/\d{1,2}/\d{4})', text)
            tanggal = tanggal.group(0) if tanggal else "Tidak Ditemukan"
            
            # 3. Cari Total Harga (Grand Total)
            # Pola: Mencari angka setelah kata "TOTAL" atau "Grand Total"
            # Ini agak tricky karena format uang bisa beda-beda
            total = re.search(r'(TOTAL|Total Tagihan|Grand Total).*?Rp\s*([\d\.,]+)', text)
            total_bersih = total.group(2) if total else "0"
            
            # Simpan ke list sementara
            data_hasil.append({
                "Nama File": file_pdf.name,
                "Nomor Dokumen": no_surat,
                "Tanggal": tanggal,
                "Total Nilai (Rp)": total_bersih
            })
            
        # Update progress bar
        progress_bar.progress((i + 1) / len(uploaded_files))

    # --- TAMPILKAN HASIL ---
    st.success("✅ Ekstraksi Selesai!")
    
    # Ubah ke DataFrame Pandas
    df = pd.DataFrame(data_hasil)
    
    # Tampilkan Tabel di Layar
    st.dataframe(df)
    
    # --- DOWNLOAD KE EXCEL ---
    # Kita gunakan Buffer (Memori sementara) agar tidak perlu simpan file ke harddisk
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data Ekstraksi')
        
    # Tombol Download
    st.download_button(
        label="📥 Download Hasil ke Excel",
        data=buffer.getvalue(),
        file_name="Rekap_Data_Invoice.xlsx",
        mime="application/vnd.ms-excel"
    )

elif not uploaded_files:
    st.info("Silakan upload file PDF terlebih dahulu.")