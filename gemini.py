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
            # FIX 1: Tambahkan toleransi agar spasi/kolom terbaca lebih rapi
            text = first_page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            
            # FIX 2: Bersihkan simbol ganda (misal: SPH//LDN -> SPH/LDN)
            text = re.sub(r'([/.-])\1+', r'\1', text)
            
            # --- LOGIKA EKSTRAKSI (REGEX DIPERBAIKI) ---
            
            # 1. Cari Nomor Invoice / Surat
            # FIX 3: Regex diperluas untuk menangkap "Invoice No", "Ref", dan titik dua (:)
            # (?i) artinya tidak peduli huruf besar/kecil
            no_surat = re.search(r'(?i)(No\.|Nomor|Invoice No\.?|Ref)\s*[:.]?\s*([A-Za-z0-9/.\-]+)', text)
            no_surat = no_surat.group(2) if no_surat else "Tidak Ditemukan"
            
            # 2. Cari Tanggal
            tanggal = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{4})', text)
            tanggal = tanggal.group(0) if tanggal else "Tidak Ditemukan"
            
            # 3. Cari Total Harga (Grand Total)
            # FIX 4: Gunakan re.DOTALL agar bisa mencari angka meskipun terpisah baris (Enter)
            # Pola: Cari Grand Total -> karakter apa saja -> Rp -> Angka
            total = re.search(r'(?i)(Grand Total|Total Tagihan|Total Payment|TOTAL).*?Rp[\.\s]*([\d\.,]+)', text, re.DOTALL)
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